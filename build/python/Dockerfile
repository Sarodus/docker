FROM python:3.5

RUN apt-get update\
    && apt-get install -y python-dev make\
    && pip install celery flower flask gunicorn