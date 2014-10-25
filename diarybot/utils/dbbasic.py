import couchdb

from diarybot.config import config
from diarybot.utils.logger import logger

import json

def store(db, docs):
    def chunker(seq, size):
        return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

    chunksize = 10000
    done = 0
    for chunk in chunker(docs, chunksize):
        db.update(chunk)
        done += chunksize
        s = "added %d of %d entries to database '%s'." % (len(docs) if len(docs) < done else done, len(docs), db.name)
        logger.debug(s)

def store_attatchment(db, key, attatchment, filename, content_type):
    db.put_attachment(key, attatchment, filename=filename, content_type=content_type)

def get_database(database_name):
    full_database_name = config.get('couchdb', 'database-prefix') + database_name
    couch = couchdb.Server(config.get('couchdb', 'database-url'))
    couch.resource.credentials = (config.get('couchdb', 'database-user'), config.get('couchdb', 'database-password'))
    db = couch[full_database_name]
    logger.debug('opening database %s' % full_database_name)
    return db

def create_database(database_name, design_document):
    full_database_name = config.get('couchdb', 'database-prefix') + database_name
    couch = couchdb.Server(config.get('couchdb', 'database-url'))
    couch.resource.credentials = (config.get('couchdb', 'database-user'), config.get('couchdb', 'database-password'))

    if full_database_name in couch:
        db = couch[full_database_name]
        logger.debug('found database %s' % full_database_name)
    else:
        db = couch.create(full_database_name)
        logger.debug('created database %s' % full_database_name)

    db['_design/diarybot'] = json.loads(design_document)
