import json
from diarybot.utils.module import Module
from diarybot.utils.logger import logger
from diarybot.utils.dbbasic import store
from diarybot.config import config

import tweepy


class Twitter(Module):
    def __init__(self):
        try:
            Module.__init__(self, "twitter")
        except:
            return

        self.screen_name = None
        self.api = self.get_api()

        self.docs = self.get_tweets()
        logger.debug("read the most recent %d tweets" % len(self.docs))
        store(self.database, self.docs)

    def get_last_stored_tweet(self):
        """
        :return: id of last stored tweet or None if no tweet was stored so far
        """
        for x in self.database.view('_design/diarybot/_view/lastid'):
            logger.debug("most recent tweet id is %d" % x['value'])
            return x['value']

        logger.debug("no previous stored tweets found - full import")
        return None

    def get_tweets(self):
        # script from https://gist.github.com/yanofsky/5436496

        all_tweets = list()

        last_stored_id = self.get_last_stored_tweet()
        oldest_tweet_id = None

        logger.debug("loading tweets...")

        while True:
            try:
                # make initial request for most recent tweets (200 is the maximum allowed count)
                new_tweets = self.api.user_timeline(screen_name=self.screen_name, count=200, max_id=oldest_tweet_id, since_id=last_stored_id)
            except tweepy.TweepError as e:
                logger.debug("got no more tweets - %s" % e.reason)
                break

            # save most recent tweets
            all_tweets.extend(json.loads(new_tweets))

            logger.debug("got %d tweets so far" % len(all_tweets))

            if not all_tweets or oldest_tweet_id == all_tweets[-1]['id'] - 1:
                break
            else:
                oldest_tweet_id = all_tweets[-1]['id'] - 1

        # add ids for CouchDB
        for tweet in all_tweets:
            tweet['_id'] = tweet['id_str']

        return all_tweets

    def get_api(self):
        """
        :return: an initialized Twitter API object
        """
        logger.debug("logging in at Twitter")

        # add a parser to access the raw JSON from the tweets
        # from http://www.hongliangjie.com/2012/04/04/hack-tweepy-to-get-raw-json/
        class RawJsonParser(tweepy.parsers.Parser):
            def parse(self, method, payload):
                return payload

        #authorize twitter, initialize Tweepy
        auth = tweepy.OAuthHandler(config.get('twitter', 'consumer_key'), config.get('twitter', 'consumer_secret'))
        auth.set_access_token(config.get('twitter', 'access_token'), config.get('twitter', 'access_token_secret'))
        api = tweepy.API(auth, parser=RawJsonParser())

        # get screen name for later access to user timeline
        self.screen_name = json.loads(api.me())['screen_name']
        logger.debug("screen name: %s" % self.screen_name)

        return api
