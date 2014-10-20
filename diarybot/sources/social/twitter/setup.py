from ....utils.logger import logger
from ....utils.dbbasic import create_database

module_name = 'twitter'

logger("creating database for module %s" % module_name)

design_document = r'''
{
   "_id": "_design/diarybot",
   "language": "javascript",
   "views": {
       "bydate": {
           "map": "function(doc) {\n    d = new Date(doc.created_at).getTime() / 1000;  \n    emit(d, doc);\n}\n"
       },
       "lastid": {
           "map": "function(doc) {\n  emit(null, doc.id);\n}",
           "reduce": "function (key, values, rereduce) {\n    var max = -Infinity;\n    for(var i = 0; i < values.length; i++)\n    {\n        if(typeof values[i] == 'number')\n        {\n            max = Math.max(values[i], max);\n        }\n    }\n    return max;\n}"
       }
   }
}
'''

create_database(module_name, design_document)
