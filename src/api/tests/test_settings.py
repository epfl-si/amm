"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf import settings
from django.test import TestCase


class KeyTestCase(TestCase):

    def get_version(self):

        self.assertEqual("0.1.5", settings.VERSION)
