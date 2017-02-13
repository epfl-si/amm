from django.test import TestCase

from api.apikey import APIKey
from api.redis import save_key, exists, get_apikeys, flushall
from config.settings.base import get_config


class RedisTestCase(TestCase):

    def test_redis(self):

        # Create data
        username = get_config("TEST_USERNAME")
        apikey = APIKey.generate()

        # Save an APIKey
        save_key(username, apikey)

        # Check is APIKEY exists
        exists(apikey.access_key, apikey.get_secret_key_hash())

        # Return all keys of username 'greg'
        keys = get_apikeys(username)

        # Check if apikey
        self.assertTrue(apikey.access_key in keys)

        flushall(self)

    def test_not_exists(self):

        # Check is APIKEY exists
        self.assertFalse(exists("1234", "4321"))
