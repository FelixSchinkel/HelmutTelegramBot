import os


class Config(object):
    TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
    GMAPS_API_KEY = os.environ.get('GMAPS_API_KEY')
