import couchdb

from diarybot.dbconfig import DATABASE_PREFIX, DATABASE_USER, DATABASE_PASS
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


def get_database(database_name):
    full_database_name = DATABASE_PREFIX + database_name
    couch = couchdb.Server()
    couch.resource.credentials = (DATABASE_USER, DATABASE_PASS)
    db = couch[full_database_name]
    logger.debug('opening database %s' % full_database_name)
    return db

def create_database(database_name, design_document):
    full_database_name = DATABASE_PREFIX + database_name
    couch = couchdb.Server()
    couch.resource.credentials = (DATABASE_USER, DATABASE_PASS)
    db = couch.create(full_database_name)
    logger.debug('created database %s' % full_database_name)
    db['_design/diarybot'] = json.loads(design_document)
