#!/usr/bin/env python

import couchdb
import json

DB_NAME = 'diarybot-nikeplus'

#############################################################################
# 1. deleting/creating the database (GENERIC)

couch = couchdb.Server()

if DB_NAME in couch:
    count = len(couch[DB_NAME])
    del couch[DB_NAME]
    print "DONE: Deleted previous database '%s' with %d entries." % (DB_NAME, count)

db = couch.create(DB_NAME)

print "DONE: Created database '%s'." % DB_NAME

#############################################################################
# 2. adding the required design documents (GENERIC)

db['_design/' + DB_NAME] = json.load(open("design_document.json"))

print "DONE: Adding design documents from 'design_document.json'."
