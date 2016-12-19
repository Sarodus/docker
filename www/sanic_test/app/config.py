from sanic.config import Config

class MyConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////data/sql.db"
