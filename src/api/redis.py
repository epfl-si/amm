from django_redis import get_redis_connection

import time


def get_connection():
    """ Get redis connection """
    return get_redis_connection("default")


def save_key(username, apikey):

    """ Save APIKey in redis """
    id = apikey.get_id(username)
    connection = get_connection()
    mapping = {
        'secret': apikey.secret_key,
        'created': time.time(),
    }
    connection.hmset(id, mapping)


def get_apikeys(username):
    """ Get all apikeys by username """

    connection = get_connection()
    apikeys = []
    for key in connection.keys('key:%s:*' % username):
        key = key.decode("utf-8")
        key_str, username, access_key = key.split(':')

        apikeys.append(access_key)
    return apikeys


def exists(access_key, secret_key):
    """ Return True if the apikey exists """

    # get the key
    key = get_connection().keys("key:*:%s" % access_key)
    key = key[0].decode("utf-8")

    key_str, username, access_key = key.split(':')

    if key and get_connection().hget(key, 'secret').decode("utf-8") == secret_key:
        return username
    return False
