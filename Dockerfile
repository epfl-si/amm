FROM python:3.6

MAINTAINER IDEVELOP <personnel.idevelop@epfl.ch>

WORKDIR /opt/amm

COPY ./requirements ./requirements/
COPY ./bin/coverage.sh ./coverage.sh
COPY ./bin/flake8.sh ./flake8.sh

ARG MAJOR_RELEASE
ARG MINOR_RELEASE
ARG BUILD_NUMBER

ENV \
    SECRET_KEY=dummy \
    TEST_CORRECT_PWD=dummy \
    TEST_WRONG_PWD=dummy \
    TEST_USERNAME=dummy \
    LDAP_USER_BASE_DN=ou=users,o=epfl,c=ch \
    LDAP_SERVER=scoldap.epfl.ch \
    LDAP_USER_SEARCH_ATTR=uid \
    CACHE_REDIS_LOCATION=redis://redis:6379/1 \
    CACHE_REDIS_CLIENT_CLASS=django_redis.client.DefaultClient \
    AMM_ENVIRONMENT=prod \
    MAJOR_RELEASE=${MAJOR_RELEASE} \
    MINOR_RELEASE=${MINOR_RELEASE} \
    BUILD_NUMBER=${BUILD_NUMBER}

RUN pip install --no-cache-dir -r requirements/local.txt
