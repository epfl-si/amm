import unittest

import utils


class LdapTest(unittest.TestCase):

    def test_auth_failed(self):

        self.assertFalse(utils.authenticate("boatto", "toto"))

