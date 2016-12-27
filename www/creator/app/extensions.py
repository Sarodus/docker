from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_cache import Cache
cache = Cache()

from flask_session import Session
sess = Session()

from celery import Celery
celery = Celery()

from .ext.creator import MyCreations
creator = MyCreations()
