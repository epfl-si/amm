FROM python:3.6

MAINTAINER IDEVELOP <personnel.idevelop@epfl.ch>

WORKDIR /opt/amm

COPY ./requirements ./requirements/
COPY secrets.json /opt/amm/secrets.json

RUN pip install --no-cache-dir -r requirements/local.txt
