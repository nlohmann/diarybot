import base64
import datetime
import time

from diarybot.utils.dbbasic import store
from diarybot.utils.logger import logger
from diarybot.utils.module import Module
from diarybot.config import config
import requests
from utils.dbbasic import store_attatchment


class InstagramDataImport(Module):
    
    client = None
    base_url = 'https://api.instagram.com/v1'

    def __init__(self):

        try:
            Module.__init__(self, "instagram")
        except:
            return

        if not self.initial_import():
            self.regular_import()

    def initial_import(self):
        """
        Import all checkins at once if no import before were executed
        :return: Boolean
        """
        if not self._get_latest_image():
            logger.debug("no local stored data found - inital import needed")

            # check how many entries in total available
            url = self.base_url+"/users/%s?access_token=%s"%(config.get('instagram','id'),config.get('instagram','access_token'))
            res = self.api_call(url)
            logger.debug("%s tracks have to be imported" % (res['data']['counts']['media']))

            self._run_fetch_store()
            return True

        return False

    def regular_import(self):
        """
        Import new checkins, beginning from the last checkin found in the local database
        :return:
        """

        latest_local_image = self._get_latest_image()

        logger.debug("latest local stored image is from %s" % datetime.datetime.fromtimestamp(int(latest_local_image['created_time'])).isoformat())

        self._run_fetch_store({'min_id':latest_local_image['id']})

        return True

    def api_call(self,url):

        r = requests.get(url)
        data = r.json()

        if data.has_key('error'):
            if data['error'] == 29:
                logger.debug("minute rate limit almost reached - wait for a minute")
                time.sleep(60)

        return data

    def _get_latest_image(self):
        """
        returns latest track
        return None if no checkin is localy stored
        :return:
        """
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=True):
            return res['value']
        return None

    def _run_fetch_store(self,params={}):
        cur_page = 0

        # at the first iteration we have to build the url by our self
        # append additional parameters
        url = self.base_url+"/users/%s/media/recent/?access_token=%s" % (config.get('instagram','id'),config.get('instagram','access_token'))+'&'+'&'.join(["%s=%s"%(k,v) for k,v in params.iteritems()])

        while True:

            # build parameter set to get step by step all data
            res = self.api_call(url)

            #store(self.database, res['data'])
            logger.debug("Stored page %s with %s images items" % (cur_page,len(res['data'])))

            for image in res['data']:
                self._get_store_attatchmend(image['id'], image['images']['standard_resolution']["url"])


            # get next url from api - if we are not at the end
            if res['pagination'].has_key('next_url'):
                url = res['pagination']['next_url']
            else:
                logger.debug("All images fetched.")
                break

        return True

    def _get_store_attatchmend(self, id, url):

        handle = requests.get(url)
        store_attatchment(self.database, [id, 'file'],base64.b64encode(handle.raw.read()) ,"standard_resolution.jpg", handle['content-type'])
        logger.debug("Stored image %s" % id)

