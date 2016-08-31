import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    REDIS_HOST = 'localhost'
    APP_HOST = '127.0.0.1'
    APP_PORT = 5000
    REDIS_PORT = 6379
    DEP_PATH = basedir + '/deploy/'