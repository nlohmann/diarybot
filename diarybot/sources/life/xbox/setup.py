from ....utils.logger import logger
from ....utils.dbbasic import create_database

module_name = 'xbox'

logger.debug("creating database for module %s" % module_name)

design_document = r'''
{
   "_id": "_design/diarybot",
   "language": "javascript",
   "views": null
}
'''

create_database(module_name, design_document)
