"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest

from django.test import tag

from auth import get_configured_authenticator
from auth.ldap import Authenticator
from config.settings.base import get_config


class LDAPTest(unittest.TestCase):

    @tag('ldap')
    def test_get_user_dn(self):
        auth = Authenticator()
        user_dn = auth.get_user_dn(username='kermit')
        self.assertEqual(user_dn, "uid=kermit,ou=users,o=epfl,c=ch")

    @tag('ldap')
    def test_authenticate(self):

        # Success test
        auth = Authenticator()
        username = get_config('TEST_USERNAME')
        password = get_config('TEST_CORRECT_PWD')
        self.assertTrue(auth.authenticate(username=username, password=password))

        # Failed test
        auth = Authenticator()
        username = None
        password = get_config('TEST_CORRECT_PWD')
        self.assertFalse(auth.authenticate(username=username, password=password))

        auth = Authenticator()
        username = 'ker|mit'
        password = get_config('TEST_CORRECT_PWD')
        self.assertFalse(auth.authenticate(username=username, password=password))

    def test_mock(self):

        from auth.mock import Authenticator
        auth = Authenticator()
        username = get_config('TEST_USERNAME')
        password = get_config('TEST_CORRECT_PWD')
        self.assertTrue(auth.authenticate(username=username, password=password))

    def test_get_configured_authenticator(self):

        auth = get_configured_authenticator()
        username = get_config('TEST_USERNAME')
        password = get_config('TEST_CORRECT_PWD')
        self.assertTrue(auth.authenticate(username=username, password=password))
