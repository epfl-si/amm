=================
AMM
=================

## Requirements

Some variables need to be assigned correctly for the application to start:

#. CACHE_REDIS_LOCATION: The django-cache connection string for the redis driver (depends on client selected)
#. CACHE_REDIS_CLIENT_CLASS: The django-cache client class to use for the redis driver (for standalone redis use: "django_redis.client.DefaultClient" )
#. SECRET_KEY: django secret key
#. LDAP_USER_SEARCH_ATTR: the LDAP user search attribute
#. LDAP_USER_BASE_DN: The BaseDN for ldap user search
#. LDAP_SERVER: The LDAP server to bind to
#. AMM_ENVIRONMENT: the amm environment


For the tests to pass, some more variables need to be assigned:

#. TEST_USERNAME: A user that exists in the LDAP
#. TEST_CORRECT_PWD: The correct password for that user for authentication
#. TEST_WRONG_PWD: A password that will fail authentication

