#!/usr/bin/env python

import couchdb
import json
import os

DB_NAME = 'diarybot-nikeplus'

#############################################################################
# 0. brute force update (should be make nicer)

couch = couchdb.Server()
db = couch[DB_NAME]

os.system('php -f get_activities.php')

data = json.load(open('activities.json', 'r'))

print 'DONE: Read %d entries' % len(data)

for entry in data:
    key = str(entry['activity']['activityId'])
    if not key in db:
        db[key] = entry

print "DONE: Added %d entries to the database '%s'." % (len(data), DB_NAME)

os.remove('activities.json')
