import unittest

from api import rancher

class RancherTest(unittest.TestCase):
    def test_create_stack(self):
        requester = "test1"
        db_username = "test2"
        db_password = "test3"
        db_port = 1234
        db_schema = "test4"
        db_stack = "test5"
        db_env = "test"

        conn = rancher.Rancher()

        ret = conn.create_stack(requester, db_username, db_password, db_port, db_schema, db_stack, db_env)
        self.assertIsNotNone(ret)

        ret = conn.get_stacks(requester)
        self.assertEqual(len(ret), 1)
        self.assertEqual(ret[0]['requester'], requester)
        self.assertEqual(ret[0]['db_username'], db_username)
        # db_password is not persisted
        self.assertEqual(ret[0]['db_port'], db_port)
        self.assertEqual(ret[0]['db_schema'], db_schema)
        self.assertEqual(ret[0]['db_stack'], db_stack)
        self.assertEqual(ret[0]['db_env'], db_env)
