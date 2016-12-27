from os import path, getenv

class Config:
    BASE_DIR = path.abspath(path.dirname(__file__)) + '/'
    SECRET_KEY = '47564h1I3r3I1hs0rAmB9R0oicSH7VM5'
    LOG_DIR = 'log/creator.log'

    SESSION_TYPE = 'redis'
    CACHE_TYPE = 'redis'

    DEBUG = True

    SQLALCHEMY_TRACK_MODIFICATI = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{db}'.format(
        user     = getenv('DB_USER'),
        password = getenv('DB_PASSWORD'),
        host     = getenv('DB_HOST'),
        db       = getenv('DEFAULT_DB'),
    )

    CACHE_REDIS_HOST = getenv('REDIS_HOST')
