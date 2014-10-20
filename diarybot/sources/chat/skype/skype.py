import sqlite3
from os.path import expanduser
from datetime import datetime

from diarybot.utils.dbbasic import store
from diarybot.utils.logger import logger
from diarybot.utils.module import Module
import diarybot.sources.chat.skype.config


class Skype(Module):
    def __init__(self):
        try:
            Module.__init__(self, "skype")
        except:
            return

        last_id = self.get_last_id()

        self.docs = [x for x in self.get_docs(last_id)]
        logger.debug("read %d new entries from Skype's local database" % len(self.docs))
        store(self.database, self.docs)

    def get_last_id(self):
        for x in self.database.view('_design/diarybot/_view/lastid'):
            logger.debug("most recent data found is from %s - incremental import" % datetime.fromtimestamp(x['value']).isoformat())
            return x['value']

        logger.debug("no previous data found - full import")
        return -1

    @staticmethod
    def get_docs(last_id):
        logger.debug("reading new entries from Skype's local database")

        db_filename = expanduser("~") + '/Library/Application Support/Skype/' + diarybot.sources.chat.skype.config.SKYPE_USERNAME + '/main.db'
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        sql_statement = '''
SELECT   author, from_dispname, timestamp, body_xml, chatname
FROM     Messages
WHERE    timestamp > {timestamp}
ORDER BY id
'''

        c.execute(sql_statement.format(timestamp=last_id))

        for entry in c.fetchall():
            yield {
                'date': datetime.fromtimestamp(entry['timestamp']).isoformat(),
                'text': entry['body_xml'],
                'author': entry['author'],
                'display_name': entry['from_dispname'],
                'chatname': entry['chatname']
            }

