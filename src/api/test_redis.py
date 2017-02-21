"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.test import TestCase

from api.apikey import APIKey
from api.redis import save_key, exists, get_apikeys, flushall
from config.settings.base import get_config


class RedisTestCase(TestCase):

    def test_redis(self):

        # create data
        username = get_config("TEST_USERNAME")
        apikey = APIKey.generate()

        # save the APIKey
        save_key(username, apikey)

        # check if the APIKey exists
        exists(apikey.access_key, apikey.get_secret_key_hash())

        # get all the keys of the test user
        keys = get_apikeys(username)

        # check that the key is there
        self.assertTrue(apikey.access_key in keys)

        flushall(self)

    def test_not_exists(self):

        # Check is APIKEY exists
        self.assertFalse(exists("1234", "4321"))
