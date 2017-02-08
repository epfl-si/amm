from django.test import TestCase

from api.apikey import APIKey


class KeyTestCase(TestCase):

    def test_generate(self):
        # Generate 100 keys and ckeck the format
        for index in range(100):
            apikey = APIKey()
            self.assertEqual(len(apikey.access_key), 20)
            self.assertEqual(len(apikey.secret_key), 40)

    def test_get_id(self):
        apikey = APIKey()
        # Check the format of the redis key
        self.assertEqual(apikey.get_id(username='greg'), "key:%s:%s" % ('greg', apikey.access_key))

    def test_to_str(self):
        apikey = APIKey()
        # Check the string representation of APIKey
        self.assertEqual(apikey.__str__(), apikey.access_key + apikey.secret_key)