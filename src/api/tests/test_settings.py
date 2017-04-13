"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
import re

from django.conf import settings
from django.test import TestCase


class KeyTestCase(TestCase):

    def test_get_version(self):
        self.assertIsNotNone(re.match('^\d+\.\d+\.\d+$', settings.VERSION))
