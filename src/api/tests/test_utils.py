"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest

from django.test import tag

from api import utils
from api.utils import get_sciper, get_units
from config.settings import base


class UtilTest(unittest.TestCase):
    def test_generate_random_b64(self):
        temp = utils.generate_random_b64(32)

        self.assertEqual(32, len(temp))

    def test_generate_password(self):
        password = utils.generate_password(32)

        self.assertEqual(32, len(password))

    def test_format_connection_string(self):
        connection = utils.get_connection_string("username", "password", "stack", "env", 1234, "schema")

        expected = "mysql://username:password@mysql.stack.env.epfl.ch:1234/schema"

        self.assertEqual(connection, expected)

    @tag('ldap')
    def test_get_sciper(self):
        sciper = get_sciper(username='kermit')
        self.assertEqual(sciper, '133134')

    @tag('ldap')
    def test_get_units(self):
        units = get_units(username=base.get_config('TEST_USERNAME'))
        self.assertEqual(len(units), 1)
        self.assertEqual("idevelop", units[0])

        units = get_units(username='ebreton')

        self.assertEqual(len(units), 3)

