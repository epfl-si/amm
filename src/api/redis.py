from django_redis import get_redis_connection


def get_connection():
    return get_redis_connection("default")


def save_apikey_in_redis(username, apikey):
    connection = get_connection()
    connection.hset('apikeys', apikey, username)


def get_apikeys(username):
    connection = get_connection()
    apikeys = []
    allkeys = connection.hgetall('apikeys')
    for key in allkeys:
        if username == connection.hget('apikeys', key):
            apikeys.append(key)
    return apikeys

def is_exist(apikey):
    connection = get_connection()
    return connection.hexists('apikeys', apikey)



