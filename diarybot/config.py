import ConfigParser

config_filename = 'diarybot.cfg'

config = ConfigParser.ConfigParser()
config.readfp(open(config_filename))
