import couchdb

from diarybot import dbconfig
from diarybot.utils.logger import logger


couch = couchdb.Server()
couch.resource.credentials = (dbconfig.DATABASE_USER, dbconfig.DATABASE_PASS)

diarybot_databases = [couch[db_name] for db_name in couch if db_name.startswith(dbconfig.DATABASE_PREFIX)]

logger.debug("performing maintenance for %d Diary Bot databases" % len(diarybot_databases))

for db in diarybot_databases:
    logger.debug("cleaning up and compacting database %s" % db.name)
    db.cleanup()
    db.compact()

    for design_document in db.view('_all_docs')['_design':'_design0']:
        # get the basename of the design document
        design_document_name = design_document.id.split('/')[-1]
        db.compact(design_document_name)

logger.debug("done")
