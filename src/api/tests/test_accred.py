import unittest
from api import accred

# the unit id for the tests
from api.accred import get_accreditations_units

UNIT_ID = "13030"

# the id of a user who has the db admin role
HAS_DB_ADMIN = "235151"

# the id of a user who has not the db admin role
HAS_NOT_ADMIN = "123456"


class AccredTest(unittest.TestCase):

    def test_is_db_admin(self):

        self.assertTrue(accred.is_db_admin(user_id=HAS_DB_ADMIN, unit_id=UNIT_ID))

        self.assertFalse(accred.is_db_admin(user_id=HAS_NOT_ADMIN, unit_id=UNIT_ID))

    def test_get_accreditations_units(self):

        units = get_accreditations_units(user_id=HAS_DB_ADMIN)
        self.assertEqual(len(units), 2)
        self.assertTrue(UNIT_ID in units)
