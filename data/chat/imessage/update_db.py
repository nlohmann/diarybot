#!/usr/bin/env python

import couchdb
import sqlite3
from os.path import expanduser
import os
from datetime import datetime
import base64

DB_NAME = 'diarybot-imessage'

#############################################################################
# 1. get last stored id from database (GENERIC)

couch = couchdb.Server()
db = couch[DB_NAME]

last_stored_id = -1
for x in db.view('_design/%s/_view/lastid' % DB_NAME):
    last_stored_id =  x['value']


#############################################################################
# 2. get the missing messages from iMessage's databse

print 'STATUS: Reading new entries from iMessage\'s local database...'

conn = sqlite3.connect(expanduser("~") + '/Library/Messages/chat.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# take care of attachments
attachment = dict()
c.execute("SELECT ROWID, filename, mime_type FROM attachment")
for entry in c:
    attachment[entry['ROWID']] = dict()
    attachment[entry['ROWID']]['filename'] = entry['filename']
    attachment[entry['ROWID']]['mime_type'] = entry['mime_type']

attachment_join = dict()
c.execute("SELECT message_id, attachment_id FROM message_attachment_join")
for entry in c:
    attachment_join[entry['message_id']] = attachment[entry['attachment_id']]

attachments_todo = []

# subtract 978307200 to convert from Apple's epoch
c.execute("SELECT message.*, handle.* FROM message INNER JOIN handle ON message.handle_id = handle.ROWID WHERE message.date > %s" % str(int(last_stored_id) - 978307200))

docs = []
attachment_count = 0
attachment_size = 0
for entry in c:
    doc = dict()
    doc['rowid'] = entry['ROWID']
    doc['id'] = entry['guid']
    # add 978307200 to convert from Apple's epoch
    doc['date'] = datetime.fromtimestamp(entry['date'] + 978307200).isoformat()
    doc['text'] = entry['text']

    if entry['is_from_me'] == 0:
        doc['from'] = entry['id']
    else:
        doc['to'] = entry['id']
    
    # if the message contains an attachment, load it and add it to the doc
    if entry['ROWID'] in attachment_join:
        attachment = attachment_join[entry['ROWID']]

        full_filename = attachment['filename'].replace('~', expanduser("~"))
        pic = open(full_filename)
        fileName, fileExtension = os.path.splitext(attachment['filename'])

        fn = "attachment" + fileExtension
        doc['_attachments'] = dict()
        doc['_attachments'][fn] = dict()
        doc['_attachments'][fn]['content_type'] = attachment['mime_type']
        doc['_attachments'][fn]['data'] = base64.b64encode(pic.read())

        attachment_count += 1
        attachment_size += len(doc['_attachments'][fn]['data'])

    doc['_id'] = entry['guid']
    docs.append(doc)

print 'DONE: Read %d new entries from iMessage\'s local database.' % len(docs)
if attachment_count > 0:
    print 'NOTE: Adding entries can be slow, because %d attachments (%d MB) are added.' % (attachment_count, attachment_size/1024/1024)

#############################################################################
# 3. store new entries in db (GENERIC) - different chunk size

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

chunksize = 100
done = 0
for chunk in chunker(docs, chunksize):
    db.update(chunk)
    done += chunksize
    print "STATUS: Added %d of %d entries to the database '%s'." % (len(docs) if len(docs) < done else done, len(docs), DB_NAME)

print "DONE: Added %d entries to the database '%s'." % (len(docs), DB_NAME)


#############################################################################
# 4. force reindex (GENERIC)

print "STATUS: Triggering re-indexing of table '%s'..." % DB_NAME
for x in db.view('_design/%s/_view/lastid' % DB_NAME):
    tmp = x['value']

print "DONE: Re-indexing of table '%s'." % DB_NAME
