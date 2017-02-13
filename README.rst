=================
AMM
=================

This application .....

http POST http://127.0.0.1:8000/v1/apikeys/ username='greg' password='toto'

HTTP/1.0 201 Created
Content-Type: application/json
Date: Fri, 03 Feb 2017 14:07:40 GMT
Server: WSGIServer/0.2 CPython/3.5.2
X-Frame-Options: SAMEORIGIN

{
    "private_key": "0e030762d7a9f0c7d20352b57f7822757824d905fd9f6fbad0d0ab15f95126ccafbe38e90df838de",
    "public_key": "c43728c2e8107da2ba4c7c492beac02e15236fcf"
}



http GET http://127.0.0.1:8000/v1/apikeys/ apikey='8b07430167658b44fa7e7a7a4ef037042a3c0be398dad50bd87dbfdda4d9946fb511844244251d365603237b634160927e0a4d56a3aca0bbc3fb0823'


## Requirements

Some variables need to be assigned correctly for the application to start:

# CACHE_REDIS_LOCATION: The django-cache connection string for the redis driver (depends on client selected)
# CACHE_REDIS_CLIENT_CLASS: The django-cache client class to use for the redis driver (for standalone redis use: "django_redis.client.DefaultClient" )
# SECRET_KEY: Unused for now ?
# LDAP_USER_BASE_DN: The BaseDN for ldap user search
# LDAP_SERVER: The LDAP server to bind to

For the tests to pass, some more variables need to be assigned:
# TEST_USERNAME: A user that exists in the LDAP
# TEST_CORRECT_PWD: The correct password for that user for authentication
# TEST_WRONG_PWD: A password that will fail authentication

