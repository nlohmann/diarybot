from diarybot.utils.module import Module
from diarybot.utils.logger import logger
from diarybot.utils.dbbasic import store
from diarybot.config import config

import iso8601
import requests
from datetime import datetime


class Xbox(Module):
    def __init__(self):
        try:
            Module.__init__(self, "xbox")
        except:
            return

        self.user_id = self.get_user_id()
        self.docs = [x for x in self.get_achievements()]
        logger.debug("read %d achievements from Xbox live" % len(self.docs))
        store(self.database, self.docs)

    def get_user_id(self):
        data = self.api_call('/v2/accountXuid')
        logger.debug("collecting data for gamer tag %s" % data['gamerTag'])
        return data['xuid']

    @staticmethod
    def api_call(endpoint):
        base_url = 'https://xboxapi.com'
        headers = {"X-AUTH": config.get('xbox', 'api_key')}
        url = base_url + endpoint
        result = requests.get(url, headers=headers)

        try:
            result = result.json()
        except ValueError:
            logger.critical("error decoding JSON: %s" % result)

        if 'error_message' in result:
            logger.critical(result['error_message'])
        return result

    def get_achievements(self):
        games_360 = self.api_call("/v2/{xuid}/xbox360games".format(xuid=self.user_id))
        games_one = self.api_call("/v2/{xuid}/xboxonegames".format(xuid=self.user_id))
        games = games_360['titles'] + games_one['titles']

        logger.debug("found %d games" % len(games))

        for game in games:
            logger.debug("processing achievements of %s" % game['name'])
            title_id = game['titleId']
            achievements = self.api_call('/v2/{xuid}/achievements/{titleId}'.format(xuid=self.user_id, titleId=title_id))

            for achievement in achievements:
                if 'unlockedOnline' in achievement:
                    achieved = achievement['unlockedOnline']
                    date = datetime.strptime(achievement['timeUnlocked'], "%Y-%m-%d %H:%M:%S")
                else:
                    achieved = (achievement['progressState'] == 'Achieved')
                    date = iso8601.parse_date(achievement['progression']['timeUnlocked'])

                if achieved:
                    achievement['parsed_date'] = date.isoformat()
                    achievement['game'] = game
                    achievement['_id'] = "%s-%d" % (title_id, achievement['id'])

                    yield achievement
