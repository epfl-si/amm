"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import time

from django_redis import get_redis_connection

from .apikey import APIKey


def get_connection():
    """
    Get a redis connection
    """
    return get_redis_connection("default")


def save_key(username, apikey):
    """
    Save the APIKey for the given user in redis
    """
    id = apikey.get_id(username)
    connection = get_connection()
    mapping = {
        'secret': apikey.secret_key_hash,
        'salt': apikey.salt.encode('utf-8'),
        'created': time.time(),
    }
    connection.hmset(id, mapping)


def get_apikeys(username):
    """
    Get all the APIKeys by username
    """
    connection = get_connection()
    apikeys = []
    for key in connection.keys('key:%s:*' % username):
        key = key.decode("utf-8")
        key_str, username, access_key = key.split(':')
        apikeys.append(access_key)
    return apikeys


def exists(access_key, secret_key):
    """
    Return True if the given APIkey exists
    """
    try:
        connection = get_connection()
        # get the key
        key = connection.keys("key:*:%s" % access_key)
        key = key[0].decode("utf-8")

        key_str, username, access_key = key.split(':')
        salt = connection.hget(key, 'salt').decode('utf-8')

        apikey = APIKey(access_key=access_key, secret_key=secret_key, salt=salt)

        if key and get_connection().hget(key, 'secret').decode("utf-8") == apikey.secret_key_hash:
            return username
        return False
    except:
        return False


def flush_all():
    """
    Flush the redis data
    """
    get_connection().flushall()
