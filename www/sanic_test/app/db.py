from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.base import app

engine = create_engine(app.config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Base.metadata.create_all(engine)
sm = sessionmaker()
sm.configure(bind=engine)
session = sm()
