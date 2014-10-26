from ....utils.logger import logger
from ....utils.dbbasic import create_database

module_name = 'foursquare'

logger.debug("creating database for module %s" % module_name)

design_document = r'''
{
   "_id": "_design/diarybot",
   "language": "javascript",
   "views": {
       "bydate": {
           "map": "function(doc) {\n  var d = new Date(doc.createdAt*1000);\n\n  emit(d.getTime() / 1000, doc);\n}"
       },
       "lastid": {
           "map": "function(doc) {\n  var d = new Date(doc.createdAt*1000);\n\n  emit(d.getTime() / 1000, doc);\n}",
           "reduce": "function (key, values, rereduce) {\n    var max = -Infinity;\n    for(var i = 0; i < values.length; i++)\n    {\n        if(typeof values[i] == 'number')\n        {\n            max = Math.max(values[i], max);\n        }\n    }\n    return max;\n}"
       }
   }
}
'''

create_database(module_name, design_document)
