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
        """
        Example:
        mysql://aa2ea71b:-CxMbtSVdPcY88MH3Vo7@mysql-78bc59f0.db.rsaas.epfl.ch:12068/98c321cb
        """
        connection = utils.get_connection_string(
            db_username="username",
            db_password="password",
            db_host="mysql-schema-id.db.rsaas.epfl.ch",
            db_port="port",
            db_schema="schema")

        expected = "mysql://username:password@mysql-schema-id.db.rsaas.epfl.ch:port/schema"

        self.assertEqual(connection, expected)

    @tag('ldap')
    def test_get_sciper(self):
        sciper = get_sciper(username='kermit')
        self.assertEqual(sciper, '133134')

    @tag('ldap')
    def test_get_units(self):

        units = get_units(username=base.get_config('TEST_USERNAME'))
        self.assertEqual(len(units), 1)
        self.assertEqual('13030', units[0])

        units = get_units(username='ebreton')
        self.assertEqual(len(units), 3)
        self.assertEqual('13029', units[0])
        self.assertEqual('13030', units[1])
        self.assertEqual('13051', units[2])
