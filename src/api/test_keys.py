from django.test import TestCase

from api.apikey import APIKey
from config.settings.base import get_config


class KeyTestCase(TestCase):

    def test_generate(self):
        # Generate 100 keys and ckeck the format
        for index in range(100):
            apikey = APIKey()
            self.assertEqual(len(apikey.access_key), 20)
            self.assertEqual(len(apikey.secret_key), 64)

    def test_get_id(self):
        apikey = APIKey()
        # Check the format of the redis key
        self.assertEqual(apikey.get_id(username=get_config("TEST_USERNAME")), "key:%s:%s" %
                (get_config("TEST_USERNAME"), apikey.access_key))

    def test_to_str(self):
        apikey = APIKey()
        # Check the string representation of APIKey
        self.assertEqual(apikey.__str__(), apikey.access_key + apikey.secret_key)

    def test_get_values(self):
        apikey = APIKey()
        self.assertEqual(len(apikey.get_values()), 2)
        self.assertTrue('secret_key' in apikey.get_values().keys())
        self.assertTrue('access_key' in apikey.get_values().keys())
