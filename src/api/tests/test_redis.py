"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.test import TestCase

from api.apikey import APIKey
from api.redis import save_key, exists, get_apikeys, flush_all
from config.settings.base import get_config

from api.apikeyhandler import ApiKeyHandler


class RedisTestCase(TestCase):

    def test_redis(self):
        # create data
        username = get_config("TEST_USERNAME")
        api_key = APIKey()

        # save the APIKey
        save_key(username, api_key)

        # check if the APIKey exists
        self.assertIsNotNone(exists(api_key.access_key, api_key.secret_key_clear))

        handler = ApiKeyHandler()

        self.assertIsNotNone(handler.validate(api_key.access_key, api_key.secret_key_clear))

        # get all the keys of the test user
        keys = get_apikeys(username)

        # check that the key is there
        self.assertTrue(api_key.access_key in keys)

        flush_all()

    def test_not_exists(self):
        # Check is APIKEY exists
        self.assertFalse(exists("1234", "4321"))
