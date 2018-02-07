import os


class Config(object):
    OPEN_MENSA_URL = 'http://openmensa.org/api/v2/canteens'

    TELEGRAM_API_KEY = os.environ.get('TELEGRAM_API_KEY')
    POSITION_LAT = os.environ.get('POS_LAT') or '51.029183'
    POSITION_LONG = os.environ.get('POS_LONG') or '13.749062'

    GMAPS_API_KEY = os.environ.get('GMAPS_API_KEY')
