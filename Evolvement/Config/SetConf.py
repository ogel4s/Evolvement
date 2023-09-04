# [Account Name] App Settings
import configparser

config = configparser.ConfigParser()

config.read('conf.ini')

account = config['ACCOUNT']['USER_NAME']