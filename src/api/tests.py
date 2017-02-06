"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.test import TestCase


class FakeTestCase(TestCase):
    def setUp(self):
        pass

    def test_fake(self):
        """Test fake"""

        self.assertEqual("toto", 'toto')
