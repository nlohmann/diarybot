from ....utils.logger import logger
from ....utils.dbbasic import create_database

module_name = 'instagram'

logger.debug("creating database for module %s" % module_name)

design_document = r'''
{
   "_id": "_design/diarybot",
   "language": "javascript",
   "views": {
       "lastid": {
           "map": "function(doc) {\n  emit(null, doc.id);\n}",
           "reduce": "function (key, values, rereduce) {\n    var max = -Infinity;\n    var smax = \"\";\n    for(var i = 0; i < values.length; i++)\n    {\n\tnmax = parseInt(values[i].split('_')[0])\n\tmax = Math.max(nmax, max);\n\tif(nmax==max){\n\t\tsmax = values[i];\n\t}\n    }\n    return smax;\n}"
       },
       "bydate": {
           "map": "function(doc) {\n    emit(doc.created_time, doc);\n}"
       }
   }
}
'''

create_database(module_name, design_document)
