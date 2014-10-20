from diarybot.utils.dbbasic import store
from diarybot.utils.logger import logger
from diarybot.utils.module import Module

import time
import datetime
import requests
from config import ACCESS_TOKEN


class Moves(Module):
    def __init__(self):
        try:
            Module.__init__(self, "moves")
        except:
            return

        self.docs = [x for x in self.get_data()]
        logger.debug("read %d new entries from the Moves API" % len(self.docs))
        store(self.database, self.docs)

    @staticmethod
    def api_call(endpoint, data):
        base_url = 'https://api.moves-app.com/api/1.1'

        r = requests.get(base_url + endpoint, params=data)

        if r.status_code == 429:
            logger.debug("rate limit exceeded, please try again in %s minutes", r.headers['x-ratelimit-minuteremaining'])

        # check rate limit
        ratelimit = int(r.headers['x-ratelimit-minuteremaining'])
        if ratelimit <= 2:
            logger.debug("minute rate limit almost reached - wait for a minute")
            time.sleep(60)

        return r.json()

    def get_first_id(self):
        """
        Query the Moves API for the first date for which data is stored for the user
        :return: a date as string formatted "%Y%m%d"
        """
        logger.debug("getting user's first date")

        endpoint = '/user/profile'
        data = {
            'access_token': ACCESS_TOKEN
        }

        res = self.api_call(endpoint, data)
        return res['profile']['firstDate']

    def get_last_id(self):
        for x in self.database.view('_design/diarybot/_view/lastid'):
            logger.debug("most recent data found is from %s - incremental import" % datetime.datetime.fromtimestamp(x['value']).isoformat())
            # add a day, because we can only get the data from up to yesterday
            return datetime.date.fromtimestamp(x['value']) + datetime.timedelta(days=1)

        logger.debug("no previous data found - full import")
        return datetime.datetime.strptime(self.get_first_id(), '%Y%m%d').date()

    def get_data(self):
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + datetime.timedelta(n)

        def get_storyline(self, date):
            logger.debug("querying story line for %s..." % date)

            endpoint = '/user/storyline/daily/%s' % date
            data = {
                'access_token': ACCESS_TOKEN,
                'trackPoints': 'true'
            }

            res = self.api_call(endpoint, data)

            # the result is a list - get the first (and only) element and add the date as id
            doc = res[0]
            doc['_id'] = date.isoformat()

            return doc

        start_date = self.get_last_id()
        end_date = datetime.date.today()

        for d in daterange(start_date, end_date):
            yield get_storyline(self, d)
