import datetime

from diarybot.utils.dbbasic import store
from diarybot.utils.logger import logger
from diarybot.utils.module import Module
from foursquare import Foursquare
from diarybot.config import config


class FoursquareDataImport(Module):
    client = None

    def __init__(self):

        try:
            Module.__init__(self, "foursquare")
        except:
            return

        self.client = Foursquare(client_id=config.get('foursquare', 'client_id'),
                                 client_secret=config.get('foursquare', 'client_secret'),
                                 redirect_uri=config.get('foursquare', 'redirect_uri'))

        self.client.set_access_token(config.get('foursquare', 'access_token'))

        if not self.initial_import():
            self.regular_import()


            # parts are needed to get an API key manually
            # auth_uri = client.oauth.auth_url()
            #print auth_uri

            #access_token = client.oauth.get_token('GA5VKWJYXPK4DLA0NGHGKXB5IMHYGKUUUO0WWQ3UYDGDYCJJ')
            #print access_token


    def initial_import(self):
        """
        Import all checkins at once if no import before were executed
        :return: Boolean
        """

        if not self._get_latest_checkin():
            logger.debug("no local stored data found - inital import needed")

            # import all checkins because we imported nothing before
            checkins = [checkin for checkin in self.client.users.all_checkins()]

            store(self.database, checkins)
            return True

        return False

    def regular_import(self):
        """
        Import new checkins, beginning from the last checkin found in the local database
        :return:
        """
        # todo: check request limit and handle exhausting
        while True:

            #+1 to get new checkins, not the same we have already
            latest_local_checkin = self._get_latest_checkin()
            latest_local_checkin_time = latest_local_checkin['createdAt'] + 1

            logger.debug("latest local stored checkin entry is from %s" % datetime.datetime.fromtimestamp(
                latest_local_checkin['createdAt']).isoformat())

            res = self.client.users.checkins(
                params={'limit': 250, 'sort': 'oldestfirst', 'afterTimestamp': (latest_local_checkin_time)})

            if len(res['checkins']['items']) == 0:
                logger.debug("no further checkins to import - finishing")
                break

            start_time = datetime.datetime.fromtimestamp(latest_local_checkin['createdAt']).isoformat()
            end_time = datetime.datetime.fromtimestamp(res['checkins']['items'][-1]['createdAt']).isoformat()

            logger.debug("store checkins from %s to %s" % (start_time, end_time))
            store(self.database, res['checkins']['items'])

        return True


    def _get_latest_checkin(self):
        """
        returns latest checkin
        return None if no checkin is localy stored
        :return:
        """
        for res in self.database.view('_design/diarybot/_view/bydate', limit=1, descending=True):
            return res['value']
        return None
