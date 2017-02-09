FROM python:3.6

MAINTAINER IDEVELOP <personnel.idevelop@epfl.ch>

WORKDIR /opt/amm

COPY ./requirements ./requirements/
COPY ./bin/coverage.sh ./coverage.sh

ENV \
    SECRET_KEY=dummy \
    TEST_CORRECT_PWD=dummy \
    TEST_WRONG_PWD=dummy \
    TEST_USERNAME=dummy \
    LDAP_USER_BASE_DN=dummy \
    LDAP_SERVER=dummy \
    CACHE_REDIS_LOCATION=dummy \
    CACHE_REDIS_CLIENT_CLASS=dummy

RUN pip install --no-cache-dir -r requirements/local.txt
