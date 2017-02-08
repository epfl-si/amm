import unittest
import utils
from config.settings.base import get_secret


class LdapTest(unittest.TestCase):

    def test_auth_failed(self):

        self.assertFalse(utils.authenticate("boatto", "toto"))

    def test_auth_successed(self):

        self.assertTrue(utils.authenticate("kermit", get_secret("TEST_PWD")))
