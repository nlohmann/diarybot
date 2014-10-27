import couchdb

from diarybot.config import config
from diarybot.utils.logger import logger

import json

def store(database, docs):
    """
    Store documents in a given database; store the documents in chunks to increase performance.
    :param database: the database to store in
    :param docs: the documents to store
    """

    def chunker(document_list, chunk_size):
        """
        Split a given document list in chunks of a given size.
        :param document_list: the list of documents
        :param chunk_size: the chunk size
        :return: a list of chunks of the document list, each with at most chunk_size elements
        """
        return (document_list[pos:pos + chunk_size] for pos in xrange(0, len(document_list), chunk_size))

    chunksize = 10000
    done = 0

    # instead of storing each document individually, store whole chunks to limit the number of HTTP calls to CouchDB
    for chunk in chunker(docs, chunksize):
        # store the chunk
        database.update(chunk)

        # print statistics
        done += len(chunk)
        s = "added %d of %d entries to database '%s'." % (len(docs) if len(docs) < done else done, len(docs), database.name)
        logger.debug(s)

def store_attatchment(db, key, attatchment, filename, content_type):
    db.put_attachment(key, attatchment, filename=filename, content_type=content_type)

def get_database(module_name):
    """
    Get a module's database from CouchDB.
    :param module_name: the name of the module for which the database shall be returned
    :return: the CouchDB database for the given module
    """
    # get the full database name from the module name and the database prefix
    full_database_name = config.get('couchdb', 'database-prefix') + module_name

    # configure the call to CouchDB
    couch = couchdb.Server(config.get('couchdb', 'database-url'))
    couch.resource.credentials = (config.get('couchdb', 'database-user'), config.get('couchdb', 'database-password'))

    # return the database
    db = couch[full_database_name]
    logger.debug('opening database %s' % full_database_name)
    return db

def create_database(module_name, design_document):
    """
    Create a database for a module and store a design document.
    :param module_name: the name of the module for which a database shall be created
    :param design_document: a design document passed from the creating module
    """

    # get the full database name from the module name and the database prefix
    full_database_name = config.get('couchdb', 'database-prefix') + module_name

    # configure the call to CouchDB
    couch = couchdb.Server(config.get('couchdb', 'database-url'))
    couch.resource.credentials = (config.get('couchdb', 'database-user'), config.get('couchdb', 'database-password'))

    # create or select the databse
    if full_database_name in couch:
        db = couch[full_database_name]
        logger.debug('found database %s' % full_database_name)
    else:
        db = couch.create(full_database_name)
        logger.debug('created database %s' % full_database_name)

    # store the passed design document
    db['_design/diarybot'] = json.loads(design_document)
