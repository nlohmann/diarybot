from diarybot.utils.logger import logger
from diarybot.utils.dbbasic import get_database
from diarybot.config import config

class Module(object):
    def __init__(self, module_name):
        logger.debug("opening module %s" % module_name)

        self.name = module_name

        # skip this module unless it is enabled in the "diarybot.cfg"
        if not config.getboolean(module_name, 'enable'):
            raise NotImplementedError

        self.database = get_database(module_name)

    def __del__(self):
        logger.debug("closing module %s\n" % self.name)
