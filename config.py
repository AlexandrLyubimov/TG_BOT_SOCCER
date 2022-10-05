"""Конфигурация программного обеспечения."""
import configparser
import os
from pathlib import Path


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

try:
    TELEGRAM_TOKEN = config.get('TELEGRAM', 'TOKEN')
    SERVER_API_URL_LEAGUE = config.get('SERVER_API', 'URL_GET_LEAGUE')
    SERVER_API_URL_TEAM = config.get('SERVER_API', 'URL_GET_TEAM')
    SERVER_API_URL_RESULT = config.get('SERVER_API', 'URL_GET_RESULT')
    SERVER_API_URL_ADD_USER = config.get('SERVER_API', 'URL_ADD_USER')
    SERVER_API_TOKEN = config.get('SERVER_API', 'TOKEN')
except configparser.ConfigParser.NoOptionError:
    print('could not read configuration file')
