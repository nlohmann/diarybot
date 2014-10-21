from ....utils.logger import logger
from ....utils.dbbasic import create_database

module_name = 'imessage'

logger.debug("creating database for module %s" % module_name)

design_document = r'''
{
   "_id": "_design/diarybot",
   "language": "javascript",
   "views": {
       "lastid": {
           "map": "function(doc) {\n    d = new Date(doc.date).getTime() / 1000;  \n    emit(null, d);\n}\n\t",
           "reduce": "function (key, values, rereduce) {\n    var max = -Infinity;\n    for(var i = 0; i < values.length; i++)\n    {\n        if(typeof values[i] == 'number')\n        {\n            max = Math.max(values[i], max);\n        }\n    }\n    return max;\n}"
       },
       "bydate": {
           "map": "function(doc) {\n    d = new Date(doc.date).getTime() / 1000;  \n    emit(d, doc);\n}\n"
       }
   }
}
'''

create_database(module_name, design_document)
