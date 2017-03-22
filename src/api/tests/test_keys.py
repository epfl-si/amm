"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.test import TestCase

from api.apikey import APIKey
from config.settings.base import get_config


class KeyTestCase(TestCase):

    def test_generate(self):
        # generate 100 keys and check the format
        for index in range(100):
            api_key = APIKey()
            self.assertEqual(len(api_key.access_key), 20)
            self.assertEqual(len(api_key.secret_key_hash), 64)
            self.assertEqual(len(api_key.salt), 20)

    def test_get_id(self):
        apikey = APIKey()
        # check the redis id format
        self.assertEqual(apikey.get_id(username=get_config("TEST_USERNAME")), "key:%s:%s" %
                         (get_config("TEST_USERNAME"), apikey.access_key))

    def test_to_str(self):
        apikey = APIKey()
        # check the string representation of APIKey
        self.assertEqual(apikey.__str__(), apikey.access_key + apikey.secret_key_hash)

    def test_get_values(self):
        apikey = APIKey()
        self.assertEqual(len(apikey.get_values()), 2)
        self.assertTrue('secret_key' in apikey.get_values().keys())
        self.assertTrue('access_key' in apikey.get_values().keys())
