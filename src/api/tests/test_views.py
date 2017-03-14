"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import json
import re

from django.urls import reverse
from rest_framework.test import APITestCase

from api import rancher
from api.redis import flushall
from api.tests import KERMIT_SCIPER
from config.settings.base import get_config


class ViewsTestCase(APITestCase):

    def setUp(self):
        flushall(self)

    def tearDown(self):
        flushall(self)

    def test_post_apikeys(self):
        """ Test the POST method of KeyView """

        response = self.client.post(
            reverse('apikeys'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(content["access_key"]), 20)
        self.assertEqual(len(content["secret_key"]), 40)

        self.assertEqual(
            response['content-type'],
            'application/json'
        )

    def test_get_apikeys(self):
        """ Test the GET method of KeyView """

        response = self.client.post(
            reverse('apikeys'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        response = self.client.get(
            reverse('apikeys'),
            data={"access_key": content["access_key"],
                  "secret_key": content["secret_key"]},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(content), 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )

    def test_post_schemas(self):
        """ Test the POST method of Schemas """

        response = self.client.post(
            reverse('apikeys'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        response = self.client.post(
            reverse('schemas'),
            data={"access_key": content["access_key"],
                  "secret_key": content["secret_key"]},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.assertIsNotNone(re.match('^mysql://\w+:[-\+\w]+@(\d+\.?)+:\d+/.+$', content['connection_string']))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )

        # Clean stacks
        conn = rancher.Rancher()
        conn.clean_stacks(KERMIT_SCIPER)

    def test_get_schemas(self):
        """ Test the GET method of schemas"""

        # create an API key
        response = self.client.post(
            reverse('apikeys'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.client.post(
            reverse('schemas'),
            data={"access_key": content["access_key"],
                  "secret_key": content["secret_key"]},
            format='json'
        )

        response = self.client.get(
            reverse('schemas'),
            data={"access_key": content["access_key"],
                  "secret_key": content["secret_key"]},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        # we get a list of dicts with 1 element
        self.assertEqual(len(content), 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )

        # Clean stacks
        conn = rancher.Rancher()
        conn.clean_stacks(KERMIT_SCIPER)

    def test_get_version(self):
        """ Test the GET method of Version """
        response = self.client.get(
                reverse('version'),
                format='json'
        )
        content = json.loads(response.content.decode('utf-8'))

        self.assertIsNotNone(re.match('^\d+\.\d+\.\d+$', content))
