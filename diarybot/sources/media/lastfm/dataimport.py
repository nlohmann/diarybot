import datetime
import time

from diarybot.utils.dbbasic import store
from diarybot.utils.logger import logger
from diarybot.utils.module import Module
from diarybot.config import config
import requests


class LastfmDataImport(Module):
    client = None
    base_url = 'http://ws.audioscrobbler.com/2.0/'

    def __init__(self):

        try:
            Module.__init__(self, "lastfm")
        except:
            return

        if not self.initial_import():
            self.regular_import()

    def initial_import(self):
        """
        Imports all tracks at once if no import before were executed
        :return: Boolean
        """
        if not self._get_latest_track():
            logger.debug("no local stored data found - inital import needed")

            params = {'method':'user.getrecenttracks',
                      'user':config.get('lastfm','username'),
                      'api_key':config.get('lastfm','api_key'),
                      'format':'json'}

            # check how many entries in total available
            data = self.api_call(params,{'limit':1})
            logger.debug("%s tracks have to be imported" % (data['recenttracks']['@attr']['total']))

            self._run_fetch_store(params)
            return True

        return False

    def regular_import(self):
        """
        Imports new tracks, beginning from the last tracks found in the local database
        :return:
        """

        # +1 to get new checkins, not the same we have already
        latest_local_track = self._get_latest_track()
        latest_local_track_time = int(latest_local_track['date']['uts']) + 1

        logger.debug("latest local stored track is from %s" % datetime.datetime.fromtimestamp(int(latest_local_track['date']['uts'])).isoformat())

        params = {'method':'user.getrecenttracks',
                  'user':config.get('lastfm','username'),
                  'api_key':config.get('lastfm','api_key'),
                  'format':'json',
                  'limit':200,
                  'from':latest_local_track_time}

        # check how many entries in total available
        short_params = params.copy()
        short_params['limit']=1

        # the result looks different, depending on whether one or more tracks are returned.
        # handle this!
        data = self.api_call(short_params)
        if data['recenttracks'].has_key('@attr'):
            logger.debug("%s tracks have to be imported" % (data['recenttracks']['@attr']['total']))
        else:
            logger.debug("%s tracks have to be imported" % (data['recenttracks']['total']))

        self._run_fetch_store(params)

        return True

    def api_call(self, min_params,opt_params={}):
        """
        handles the API calls and errors
        :param url: full url to API endpoint
        :return: json-data
        """

        r = requests.get(self.base_url, params=dict(min_params.items()+opt_params.items()))
        data = r.json()

        # do it in a better way (chicking rate-limit etc)
        if data.has_key('error'):
            if data['error'] == 29:
                logger.debug("minute rate limit almost reached - wait for a minute")
                time.sleep(60)

        return data

    def _get_latest_track(self):
        """
        returns latest track
        return None if no checkin is locally stored
        :return:
        """
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=True):
            return res['value']
        return None

    def _run_fetch_store(self,param):
        """
        fetches available tracks from lastfm page by page and stores inside the database
        :param params: parameter to narrow the API result
        :return: True
        """

        next_page=1

        while True:

            # build parameter set to get step by step all data
            opt_params = {'extended':1,
                          'page':next_page
                          }

            data = self.api_call(param,opt_params)

            if data['recenttracks'].has_key('@attr'):
                attr = data['recenttracks']['@attr']
            else:
                attr = data['recenttracks']

            # stop import process if we do not have any import!
            if int(attr['total']) == 0:
                break


            # when we get a single track it is not a list so wie have fix this manually
            tracks = data['recenttracks']['track']
            if not isinstance(tracks,list):
                tracks = list(data['recenttracks']['track'])

            store(self.database, tracks)
            logger.debug("Stored page %s with %s tracks" % (attr['page'],len(data['recenttracks']['track'])))

            # calculate next iteration
            cur_page = int(attr['page'])
            if cur_page<int(attr['totalPages']):
                next_page = cur_page+1
            else:
                logger.debug("All tracks fetched.")
                break

        return True