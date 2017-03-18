"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest

from auth.ldap import Authenticator
from config.settings.base import get_config


class LDAPTest(unittest.TestCase):

    def test_get_user_dn(self):
        auth = Authenticator()
        user_dn = auth.get_user_dn(username='kermit')
        self.assertEqual(user_dn, "uid=kermit,ou=users,o=epfl,c=ch")

    def test_authenticate(self):
        auth = Authenticator()
        username = get_config('TEST_USERNAME')
        password = get_config('TEST_CORRECT_PWD')
        self.assertTrue(auth.authenticate(username=username, password=password))
