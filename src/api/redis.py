from django_redis import get_redis_connection


def get_connection():
    return get_redis_connection("default")


def save_in_redis(username, key):
    connection = get_connection()
    connection.lpush(username, key)


def get_keys(username):
    connection = get_connection()
    return connection.lrange(username, 0, -1)


def get_all_keys():
    connection = get_connection()
    return connection.keys()
