"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import unittest
from api import rancher
from api.tests import KERMIT_SCIPER


class RancherTest(unittest.TestCase):

    def test_get(self):

        conn = rancher.Rancher()

        r = conn.get("/v1-catalog/templates/idevelop:mysql")

        self.assertEqual(200, r.status_code)

    def test_get_template(self):

        conn = rancher.Rancher()

        template = "idevelop:mysql"

        data = conn.get_template(template)

        self.assertTrue(data["id"].startswith(template))

    def test_create_mysql_stack(self):

        conn = rancher.Rancher()
        data = conn.create_mysql_stack(KERMIT_SCIPER)

        self.assertTrue(data["connection_string"].startswith("mysql://"))
        self.assertTrue(data["mysql_cmd"].startswith("mysql "))

        # Return stacks by sciper
        conn.get_stacks(KERMIT_SCIPER)

        # Clean stacks
        conn.clean_stacks(KERMIT_SCIPER)

    def test_get_available_port(self):

        conn = rancher.Rancher()
        conn.get_available_port()

    def test_get_stacks(self):

        # Create new stacks
        conn = rancher.Rancher()

        conn.create_mysql_stack(KERMIT_SCIPER)
        conn.create_mysql_stack(KERMIT_SCIPER)

        # Return stacks by sciper
        stacks = conn.get_stacks(KERMIT_SCIPER)

        # Check the number of stacks
        self.assertEqual(len(stacks), 2)

        # Clean stacks
        conn.clean_stacks(KERMIT_SCIPER)

    def test_get_schemas(self):

        # Create new stacks
        conn = rancher.Rancher()
        conn.create_mysql_stack(KERMIT_SCIPER)
        conn.create_mysql_stack(KERMIT_SCIPER)

        # Return schemas by sciper
        schemas = conn.get_schemas(KERMIT_SCIPER)

        # Check the number of stacks
        self.assertEqual(len(schemas), 2)

        # Return stacks by sciper
        conn.get_stacks(KERMIT_SCIPER)

        # Clean stacks
        conn.clean_stacks(KERMIT_SCIPER)
