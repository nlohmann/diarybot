from diarybot.utils.logger import logger
from diarybot.utils.dbbasic import get_database


class Module(object):
    def __init__(self, module_name):
        logger.debug("opening module %s" % module_name)

        self.name = module_name
        self.database = get_database(module_name)

    def __del__(self):
        logger.debug("closing module %s" % self.name)
