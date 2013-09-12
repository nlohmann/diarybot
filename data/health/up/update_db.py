#!/usr/bin/env python

import couchdb
import json
import urllib
import urllib2
from cookielib import CookieJar

# load configuration
CONFIG = json.load(open('config.json'))

DB_NAME = 'diarybot-up'


#############################################################################
# 2. get data from Jawbone's inofficial API

print 'STATUS: Reading entries from Jawbone\'s API...'

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

url = 'https://jawbone.com/user/signin/login'
values = {'email' : CONFIG['username'], 'pwd': CONFIG['password'], 'service': 'nudge'}
data = urllib.urlencode(values)
response = opener.open(url, data)

baseurl = 'https://jawbone.com'
nexturl = '/nudge/api/v.1.33/users/@me/social?limit=1000'

all_data = []
while True:
    response = opener.open(baseurl + nexturl)
    r = response.read()
    j = json.loads(r)
    all_data += j['data']['feed']

    try:
        nexturl = j['data']['links']['next']
    except:
        break

print 'STATUS: Fetching further information...'

for data in all_data:
    if data['type'] == 'sleep':
        url = 'https://jawbone.com/nudge/api/v.1.33/sleeps/%s/snapshot' % data['xid']
        response = opener.open(url)
        data['snapshot'] = json.loads(response.read())['data']

    if data['type'] == 'move':
        url = 'https://jawbone.com/nudge/api/v.1.33/moves/%s/snapshot' % data['xid']
        response = opener.open(url)
        data['snapshot'] = json.loads(response.read())['data']

print 'DONE: Read %d entries from Jawbone\'s API.' % len(all_data)-1

#############################################################################
# 3. store new entries in db (ADJUSTED: should be a bulk update)

couch = couchdb.Server()
db = couch[DB_NAME]

counter = 0
for entry in all_data:
    try:
        key = str(entry['xid'])
        if not key in db:
            db[key] = entry
            counter += 1
    except:
        continue

print "DONE: Added %d entries to the database '%s'." % (counter, DB_NAME)
