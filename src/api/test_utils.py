"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest

from api import utils
# from config.settings.base import get_config


class UtilTest(unittest.TestCase):

    def test_generate_random_b64(self):

        temp = utils.generate_random_b64(32)

        self.assertEqual(32, len(temp))

    def test_generate_password(self):

        password = utils.generate_password(32)

        self.assertEqual(32, len(password))

#    def test_auth_failed(self):
#
#        self.assertFalse(utils.authenticate(get_config("TEST_USERNAME"), get_config("TEST_WRONG_PWD")))
#
#    def test_auth_successed(self):
#
#        self.assertTrue(utils.authenticate(get_config("TEST_USERNAME"), get_config("TEST_CORRECT_PWD")))
