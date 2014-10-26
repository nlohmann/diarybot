import base64
import datetime
import time
import urllib2

from diarybot.utils.logger import logger
from diarybot.utils.module import Module
from diarybot.config import config
import requests

class InstagramDataImport(Module):
    
    client = None
    meta_local_image_count = 0
    meta_online_image_count = 0
    base_url = 'https://api.instagram.com/v1'

    def __init__(self):

        try:
            Module.__init__(self, "instagram")
        except:
            return

        # get meta infos
        self.meta_local_image_count = self._get_local_image_count()
        self.meta_online_image_count = self._get_online_image_count()

        if not self.initial_import():
            self.regular_import()

    def initial_import(self):
        """
        Import all checkins at once if no import before were executed
        :return: Boolean
        """
        if not self._get_latest_image():
            logger.debug("no local stored data found - inital import needed")
            logger.debug("%s tracks have to be imported" % self.meta_local_image_count)

            self._run_fetch_store()
            return True

        return False

    def regular_import(self):
        """
        Import new checkins, beginning from the last checkin found in the local database
        :return:
        """

        latest_local_image = self._get_latest_image()
        first_local_image = self._get_first_image()

        # check if we have imported all images previews the oldes we have
        url = self.base_url+"/users/%s/media/recent/?access_token=%s&min_id=%s"%(config.get('instagram','id'),config.get('instagram','access_token'),first_local_image['id'])
        res = self._api_call(url)

        if len(res['data'])>0:
            self._run_fetch_store({'min_id':first_local_image['id']})

        # now import all newer images thince the newest we have
        logger.debug("latest local stored image is from %s" % datetime.datetime.fromtimestamp(int(latest_local_image['created_time'])).isoformat())
        self._run_fetch_store({'max_id':latest_local_image['id']})

        return True

    def _api_call(self,url):

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

    def _get_first_image(self):
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=False):
            return res['value']
        return None

    def _get_local_image_count(self):
        t = self.database.view('_design/diarybot/_view/imagecount', limit=1, reduce=True)
        if len(t.rows)>0:
            return t.rows[0]['value']
        return 0

    def _get_online_image_count(self):
        # check how many entries in total available
        url = self.base_url+"/users/%s?access_token=%s"%(config.get('instagram','id'),config.get('instagram','access_token'))
        res = self._api_call(url)
        return int(res['data']['counts']['media'])

    def _run_fetch_store(self,params={}):

        record_count = 0

        # at the first iteration we have to build the url by our self
        # append additional parameters
        url = self.base_url+"/users/%s/media/recent/?access_token=%s" % (config.get('instagram','id'),config.get('instagram','access_token'))+'&'+'&'.join(["%s=%s"%(k,v) for k,v in params.iteritems()])

        while True:

            # build parameter set to get step by step all data
            res = self._api_call(url)

            self._store_wattatchment(self.database, res['data'] )
            record_count = record_count + len(res['data'])
            logger.debug("Stored %s of in total %s images in database" % (record_count, (self.meta_online_image_count-self.meta_local_image_count)))

            # get next url from api - if we are not at the end
            if res['pagination'].has_key('next_url'):
                url = res['pagination']['next_url']
            else:
                logger.debug("All images fetched.")
                break

        return True

    def _store_wattatchment(self, db, docs):
        # store json with main data
        store_results = db.update(docs)

        # attatch binary image to it database record
        for db_res in store_results:
            # extract attatchmend date from json object
            doc = self.database.get(db_res[1])
            file = requests.get(doc['images']['standard_resolution']['url'])
            b64 = base64.b64encode(file.content)
            key = {'_id':db_res[1], '_rev':db_res[2]}
            db.put_attachment(key, b64, filename="standard_resolution.jpg", content_type=file.headers['content-type'])

            if doc['caption']:
                text = doc['caption']['text']
            else:
                text = "untitled"

            logger.debug('Attached "%s" image' % text)

        #s = "added %d of %d entries to database '%s'." % (len(docs) if len(docs) < done else done, len(docs), db.name)
        logger.debug("import photo is done.")
