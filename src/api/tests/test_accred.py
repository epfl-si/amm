import unittest

from django.test import tag

from api.accred import is_db_admin, get_accreditations_units


class AccredTest(unittest.TestCase):

    # the unit id for the tests
    UNIT_ID = "13030"

    # the id of a user who has the db admin role
    HAS_DB_ADMIN = "235151"

    # the id of a user who has not the db admin role
    HAS_NOT_ADMIN = "123456"

    @tag('accred')
    def test_is_db_admin(self):

        self.assertTrue(is_db_admin(user_id=self.HAS_DB_ADMIN, unit_id=self.UNIT_ID))

        self.assertFalse(is_db_admin(user_id=self.HAS_NOT_ADMIN, unit_id=self.UNIT_ID))

    @tag('accred')
    def test_get_accreditations_units(self):

        units = get_accreditations_units(user_id=self.HAS_DB_ADMIN)
        self.assertEqual(len(units), 2)
        self.assertTrue(self.UNIT_ID in units)
