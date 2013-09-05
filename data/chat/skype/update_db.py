#!/usr/bin/env python

import couchdb
import sqlite3
from os.path import expanduser
from datetime import datetime
import json

# load configuration
CONFIG = json.load(open('config.json'))

DB_NAME = 'diarybot-skype'

#############################################################################
# 1. get last stored id from database (GENERIC)

couch = couchdb.Server()
db = couch[DB_NAME]

last_stored_id = 0
for x in db.view('_design/%s/_view/lastid' % DB_NAME):
    last_stored_id =  x['value']


#############################################################################
# 2. get the missing messages from Skype's databse

print 'STATUS: Reading new entries from Skype\'s local database...'

conn = sqlite3.connect(expanduser("~") + '/Library/Application Support/Skype/' + CONFIG['skype_username'] + '/main.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("SELECT author, from_dispname, timestamp, body_xml, chatname FROM Messages WHERE timestamp > %d ORDER BY id" % last_stored_id)

docs = []
for entry in c:
    doc = dict()
    doc['date'] = datetime.fromtimestamp(entry['timestamp']).isoformat()
    doc['text'] = entry['body_xml']
    doc['author'] = entry['author']
    doc['display_name'] = entry['from_dispname']
    doc['chatname'] = entry['chatname']
    docs.append(doc)

print 'DONE: Read %d new entries from Skype\'s local database.' % len(docs)

#############################################################################
# 3. store new entries in db (GENERIC)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

chunksize = 10000
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
