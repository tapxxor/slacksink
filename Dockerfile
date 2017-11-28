FROM python:3.5.4-alpine

MAINTAINER Theofanis Pispirigkos <theofanis.pispirigkos@metis.tech>

RUN apk update \
 && apk upgrade \
 && apk add bash \
 && apk add bash-completion \
 && python3 -m ensurepip \
 && rm /var/cache/apk/*

RUN mkdir /app

WORKDIR /app

ADD dependencies .

RUN pip3 install -r dependencies

ADD . /app

ENTRYPOINT ["python3","/app/src/app.py"]