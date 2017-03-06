=================
AMM
=================

Requirements
============

Create a .env file on the project's root with the following variables :

#. CACHE_REDIS_LOCATION: The django-cache connection string for the redis driver (depends on client selected)
#. CACHE_REDIS_CLIENT_CLASS: The django-cache client class to use for the redis driver (for standalone redis use: "django_redis.client.DefaultClient" )
#. SECRET_KEY: django secret key
#. LDAP_USER_SEARCH_ATTR: the LDAP user search attribute
#. LDAP_USER_BASE_DN: The BaseDN for ldap user search
#. LDAP_SERVER: The LDAP server to bind to
#. LDAP_USE_SSL: Whether to use 'ldaps' or 'ldap' (no support for starttls), use 'ldaps' only if set to 'true' any other value is false
#. AMM_ENVIRONMENT: the amm environment
#. AMM_AUTHENTICATOR_CLASS: The authentication class to use, currently only 'ldap' is supported
#. DJANGO_HOST: the value to accept as Host header in HTTP requests
#. DJANGO_WORKER_COUNT: the number of worker processes
#. DJANGO_SETTINGS_MODULE: the django configuration module to use, currently only 'config.settings.local' for local testing and 'config.settings.base' for production are supported
#. RANCHER_API_URL: the base URL to access the Rancher API
#. RANCHER_VERIFY_CERTIFICATE: if true the Rancher SSL certificate will be verified
#. RANCHER_ACCESS_KEY: the Rancher API access key
#. RANCHER_SECRET_KEY: the Rancher API secret key

For the tests to pass, some more variables need to be assigned:

#. TEST_USERNAME: A user that exists in the LDAP
#. TEST_CORRECT_PWD: The correct password for that user for authentication
#. TEST_WRONG_PWD: A password that will fail authentication

Version Number:

The version number is set using the following environment variables:

# MAJOR_RELEASE: The major version of the application
# MINOR_RELEASE: The bugfix version of the application
# BUILD_NUMBER: The build number, which should be incremented at each image build

These variables are setup when the image is built using variables of the exact same name set with --build-arg. The build system is responsible for setting these variables correctly in the docker ``build command``.

(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
