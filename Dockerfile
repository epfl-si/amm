FROM python:3.6

MAINTAINER IDEVELOP <personnel.idevelop@epfl.ch>

WORKDIR /opt/amm

COPY ./requirements ./requirements/
COPY secrets.json ./secrets.json
COPY ./bin/coverage.sh ./coverage.sh

RUN pip install --no-cache-dir -r requirements/local.txt
