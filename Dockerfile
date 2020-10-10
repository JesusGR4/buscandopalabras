FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN apt-get upgrade && apt-get update && apt-get install --assume-yes default-libmysqlclient-dev python3-pip python-dev python3-dev && pip3 install --upgrade pip && pip3 install -r /config/requirements.pip && mkdir /app
WORKDIR /app