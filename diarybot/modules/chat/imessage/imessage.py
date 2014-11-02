from diarybot.utils.dbbasic import store
from diarybot.utils.module import Module
from diarybot.utils.logger import logger

import sqlite3
from os.path import expanduser, basename, isdir
import os
from datetime import datetime
import base64
import tempfile
import shutil


class Imessage(Module):
    def __init__(self):
        try:
            Module.__init__(self, "imessage")
        except:
            return

        last_id = self.get_last_id()
        self.docs = [x for x in self.get_docs(last_id)]
        logger.debug("read %d new entries from iMessage's local database" % len(self.docs))
        store(self.database, self.docs)

    def get_last_id(self):
        for x in self.database.view('_design/diarybot/_view/lastid'):
            logger.debug("most recent data found is from %s - incremental import" % datetime.fromtimestamp(x['value']).isoformat())
            return x['value']

        logger.debug("no previous data found - full import")
        return -1

    @staticmethod
    def get_docs(last_id):
        """
        Query the iMessage database for new messages.

        :param last_id: the timestamp of the first document to create
        :return: a generator for documents in JSON format suitable for CouchDB
        """

        def unix2apple(timestamp):
            """
            Apple handles timestamps differently. Whereas the unix epoch is 1970-01-01T00:00:00, the
            Apple epoch is 2001-01-01T00:00:00.

            :param timestamp: a UNIX timestamp (seconds since epoch)
            :return: an Apple timestamp
            """
            return timestamp - 978307200

        def apple2unix(timestamp):
            """
            Apple handles timestamps differently. Whereas the unix epoch is 1970-01-01T00:00:00, the
            Apple epoch is 2001-01-01T00:00:00.

            :param timestamp: an Apple timestamp (seconds since 2001-01-01)
            :return: a UNIX timestamp
            """
            return timestamp + 978307200

        def get_attachments(message_id, connection):
            """
            Query the iMessage database for attachments for a message.

            :param message_id: the id of the message to get attachments for
            :param connection: a connection to the iMessage SQLite database
            :rtype : a generator for the attachments in CouchDB JSON format
            """
            sql_statement = '''
SELECT attachment.ROWID, attachment.filename, attachment.mime_type,
       message_attachment_join.message_id
FROM   attachment, message_attachment_join
WHERE  attachment.ROWID = message_attachment_join.attachment_id AND
       message_attachment_join.message_id = {message_id}
'''
            c = connection.cursor()
            c.execute(sql_statement.format(message_id=message_id))
            for entry in c.fetchall():
                full_filename = entry['filename'].replace('~', expanduser("~"))

                if isdir(full_filename):
                    # create a ZIP file of the directory in a temp dir
                    tempdir_name = tempfile.mkdtemp()
                    zip_filename = os.path.join(tempdir_name, basename(full_filename))
                    shutil.make_archive(zip_filename, 'zip', os.path.dirname(full_filename))
                    zip_filename += '.zip'

                    handle = open(zip_filename)
                    yield {
                        basename(zip_filename): {
                            'content_type': 'application/zip',
                            'data': base64.b64encode(handle.read())
                        }
                    }

                    # tidy up temporary zip file
                    shutil.rmtree(tempdir_name)

                else:
                    handle = open(full_filename)
                    yield {
                        basename(entry['filename']): {
                            'content_type': entry['mime_type'],
                            'data': base64.b64encode(handle.read())
                        }
                    }

        logger.debug("reading new entries from iMessage's local database")

        # connect to the iMessage database
        db_filename = expanduser("~") + '/Library/Messages/chat.db'
        conn = sqlite3.connect(db_filename)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # query all messages since given timestamp
        sql_statement = """
SELECT     message.ROWID, message.guid, message.date, message.text, message.is_from_me, handle.id
FROM       message
INNER JOIN handle ON message.handle_id = handle.ROWID
WHERE      message.date > {last_date}
"""
        c.execute(sql_statement.format(last_date=unix2apple(last_id)))

        for entry in c:
            # prepare a document for CouchDB
            doc = dict()
            doc['rowid'] = entry['ROWID']
            doc['id'] = entry['guid']
            doc['date'] = datetime.fromtimestamp(apple2unix(entry['date'])).isoformat()
            doc['text'] = entry['text']

            if entry['is_from_me'] == 0:
                doc['from'] = entry['id']
            else:
                doc['to'] = entry['id']

            # collect attachments
            attachments = [x for x in get_attachments(entry['ROWID'], conn)]
            if attachments:
                doc['_attachments'] = dict()
                for attachment in attachments:
                    doc['_attachments'].update(attachment)

            doc['_id'] = entry['guid']
            yield doc
