FROM python:2-alpine

RUN apk --update upgrade \
    && apk add openssl curl ca-certificates python-dev gcc musl-dev git openssh-client libxslt-dev libxml2-dev\
    && update-ca-certificates \
    && pip install celery flower gunicorn
