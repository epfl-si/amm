"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import unittest

from django.test import tag
from rest_framework.exceptions import ValidationError

from api.serializers import SchemaSerializer


class SchemaSerializerTest(unittest.TestCase):

    @tag('ldap')
    def test_manage_units(self):

        # User has only one unit
        unit = "13030"
        result = SchemaSerializer._manage_units(username="kermit", unit=unit, result={})
        self.assertEqual(unit, result["unit"])

        result = SchemaSerializer._manage_units(username="kermit", unit=None, result={})
        self.assertEqual(unit, result["unit"])

        # Bad unit
        unit = "13031"
        try:
            result = SchemaSerializer._manage_units(username="kermit", unit=unit, result={})
        except ValidationError as error:
            self.assertEqual('Bad unit', error.detail[0])

        # User has many units
        try:
            result = SchemaSerializer._manage_units(username="ebreton", unit=None, result={})
        except ValidationError as error:
            self.assertTrue(error.detail[0].startswith("User has more one unit"))
