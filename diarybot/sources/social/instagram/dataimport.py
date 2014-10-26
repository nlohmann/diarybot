import base64
import datetime
import time

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
        self.meta_local_image_count = self._get_local_media_count()
        self.meta_online_image_count = self._get_online_media_count()

        if not self.initial_import():
            self.regular_import()

    def initial_import(self):
        """
        Import all images and movies at once if no import before were executed
        :return: Boolean
        """
        if not self._get_latest_media():
            logger.debug("no local stored data found - inital import needed")
            logger.debug("%s tracks have to be imported" % self.meta_local_image_count)

            self._run_fetch()
            return True

        return False

    def regular_import(self):
        """
        Import new images and moves
        Check first if all old media files were imported. This can happen when the import will be interrupted.
        Then check if newer media files exists and import them
        :return:
        """

        latest_local_image = self._get_latest_media()
        first_local_image = self._get_first_media()

        # check if we have imported all images previews the oldes we have
        url = self.base_url+"/users/%s/media/recent/?access_token=%s&max_id=%s"%(config.get('instagram','id'),config.get('instagram','access_token'),first_local_image['id'])
        res = self._api_call(url)

        if len(res['data'])>0:
            self._run_fetch({'min_id':first_local_image['id']})

        # now import all newer images thince the newest we have
        logger.debug("latest local stored image is from %s" % datetime.datetime.fromtimestamp(int(latest_local_image['created_time'])).isoformat())
        self._run_fetch({'min_id':latest_local_image['id'],'max_timestamp':latest_local_image['created_time']})

        return True

    def _api_call(self,url):
        """
        handles the API calls and errors
        :param url: full url to API endpoint
        :return: json-data
        """

        r = requests.get(url)
        data = r.json()

        # do it in a better way (chicking rate-limit etc)
        if data.has_key('error'):
            if data['error'] == 29:
                logger.debug("minute rate limit almost reached - wait for a minute")
                time.sleep(60)

        return data

    def _get_latest_media(self):
        """
        returns latest media database record
        returns None if no media were locally stored
        :return:
        """
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=True):
            return res['value']
        return None

    def _get_first_media(self):
        """
        returns oldest media database record
        returns None if no media were locally stored
        :return:
        """
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=False):
            return res['value']
        return None

    def _get_local_media_count(self):
        """
        returns the total count of local media recoreds
        :return:
        """
        t = self.database.view('_design/diarybot/_view/imagecount', limit=1, reduce=True)
        if len(t.rows)>0:
            return t.rows[0]['value']
        return 0

    def _get_online_media_count(self):
        """
        returns total online available media count
        :return:
        """
        # check how many entries in total available
        url = self.base_url+"/users/%s?access_token=%s"%(config.get('instagram','id'),config.get('instagram','access_token'))
        res = self._api_call(url)
        return int(res['data']['counts']['media'])

    def _run_fetch(self,params={}):
        """
        fetches available media from instagram page by page
        :param params: parameter to narrow the API result
        :return: True
        """

        record_count = 0

        # at the first iteration we have to build the url by our self
        # append additional parameters
        url = self.base_url+"/users/%s/media/recent/?access_token=%s" % (config.get('instagram','id'),config.get('instagram','access_token'))+'&'+'&'.join(["%s=%s"%(k,v) for k,v in params.iteritems()])

        while True:

            # build parameter set to get step by step all data
            res = self._api_call(url)

            # break here if there is nothing to import
            if len(res['data'])<1:
                logger.debug("nothing to import.")
                break

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
        """
        stores the API result, fetches for each of it the media file and saves it base64encoded aside each record.
        :param db: database handle
        :param docs: API result
        :return:
        """

        if len(docs)<1:
            logger.debug("nothing to import.")
            return False

        # store json with main data
        store_results = db.update(docs)

        # attatch binary image to it database record
        for db_res in store_results:
            # extract attatchmend date from json object
            doc = self.database.get(db_res[1])
            file = requests.get(doc['images']['standard_resolution']['url'])
            key = {'_id':db_res[1], '_rev':db_res[2]}
            db.put_attachment(key, file.content, filename="standard_resolution.jpg", content_type=file.headers['content-type'])

            if doc['caption']:
                text = doc['caption']['text']
            else:
                text = "untitled"

            logger.debug('Attached "%s" image' % text)

        logger.debug("import photo is done.")
        return True