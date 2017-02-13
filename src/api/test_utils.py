import unittest

from api import utils
from config.settings.base import get_config


class LdapTest(unittest.TestCase):

    def test_auth_failed(self):

        self.assertFalse(utils.authenticate(get_config("TEST_USERNAME"), get_config("TEST_WRONG_PWD")))

    def test_auth_successed(self):

        self.assertTrue(utils.authenticate(get_config("TEST_USERNAME"), get_config("TEST_CORRECT_PWD")))
