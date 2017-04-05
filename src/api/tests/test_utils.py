"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest

from django.test import tag

from api import utils
from api.utils import get_sciper, get_units, is_unit_exist, get_username, get_unit_name
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

        # with password
        connection = utils.get_connection_string(
            db_username="username",
            db_password="password",
            db_host="mysql-schema-id.db.rsaas.epfl.ch",
            db_port="port",
            db_schema="schema")

        expected = "mysql://username:password@mysql-schema-id.db.rsaas.epfl.ch:port/schema"

        self.assertEqual(connection, expected)

        # without password
        connection = utils.get_connection_string(
            db_username="username",
            db_password=None,
            db_host="mysql-schema-id.db.rsaas.epfl.ch",
            db_port="port",
            db_schema="schema")

        expected = "mysql://username@mysql-schema-id.db.rsaas.epfl.ch:port/schema"

        self.assertEqual(connection, expected)

    def test_format_mysql_cmd(self):

        # with password
        cmd = utils.get_mysql_client_cmd(
            db_username="username",
            db_password="password",
            db_host="mysql-schema-id.db.rsaas.epfl.ch",
            db_port="port",
            db_schema="schema")

        expected = "mysql -h mysql-schema-id.db.rsaas.epfl.ch -uusername -ppassword -P port schema"

        self.assertEqual(cmd, expected)

        # without password
        cmd = utils.get_mysql_client_cmd(
            db_username="username",
            db_password=None,
            db_host="mysql-schema-id.db.rsaas.epfl.ch",
            db_port="port",
            db_schema="schema")

        expected = "mysql -h mysql-schema-id.db.rsaas.epfl.ch -uusername -p -P port schema"

        self.assertEqual(cmd, expected)

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

    @tag('ldap')
    def test_is_unit_exist(self):

        # Success
        self.assertTrue(is_unit_exist(unit_id='13030'))

        # Fail
        self.assertFalse(is_unit_exist(unit_id='88'))

    @tag('ldap')
    def test_get_username(self):

        username = get_username(sciper='133134')
        self.assertEqual(username, 'kermit')

    @tag('ldap')
    def test_get_unit_name(self):
        unit = get_unit_name(unit_id='13030')
        self.assertEqual(unit.lower(), 'idevelop')
