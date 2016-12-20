FROM python:3.5-alpine

RUN apk --update upgrade \
    && apk add openssl curl ca-certificates python-dev gcc musl-dev git openssh-client libxslt-dev libxml2-dev g++ make\
    && apk add python-dev