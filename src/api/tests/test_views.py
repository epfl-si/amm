"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import json
import re
from time import sleep

from django.test import tag
from django.urls import reverse
from rest_framework.test import APITestCase

from api import rancher
from api.redis import flush_all
from api.tests import KERMIT_SCIPER, KERMIT_UNIT
from config.settings.base import get_config


class ViewsTestCase(APITestCase):

    def setUp(self):
        flush_all()

    def tearDown(self):
        flush_all()

    def test_get_unit_list(self):

        response = self.client.get(
            reverse('unit-list'),
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, "Units not found")

    def test_get_user_list(self):

        response = self.client.get(
            reverse('user-list'),
            data={},
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, "Users not found")

    def test_get_user_detail(self):

        response = self.client.get(
            reverse(viewname='user-detail', args={'user_id': "133134"}),
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, "User not found")

    def test_get_unit_detail(self):

        response = self.client.get(
            reverse(viewname='unit-detail', args={'unit_id': KERMIT_UNIT}),
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content, "Unit not found")

    def test_post_apikeys(self):
        """
        Test the POST method of KeyView
        """

        response = self.client.post(
            reverse('apikey-list'),
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
            reverse('apikey-list'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        response = self.client.get(
            reverse('apikey-list'),
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

    @tag('rancher')
    def test_post_schemas(self):
        """ Test the POST method of Schemas """

        # create API Keys
        response = self.client.post(
            reverse('apikey-list'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))
        access_key = content["access_key"]
        secret_key = content["secret_key"]

        # create schemas
        response = self.client.post(
            reverse('schema-list'),
            data={"access_key": access_key,
                  "secret_key": secret_key},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        "mysql://aa2ea71b:-CxMbtSVdPcY88MH3Vo7@mysql-78bc59f0.db.rsaas.epfl.ch:12068/98c321cb"
        self.assertIsNotNone(re.match('^mysql://\w+:[-\+\w]+@[-\.\w]+:\d+/.+$', content['connection_string']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )

        # Get schema
        response = self.client.get(
            reverse(
                viewname='schema-detail',
                args={content["schema_id"]},
            ),
            data={"access_key": access_key, "secret_key": secret_key},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        self.assertIsNotNone(re.match('^mysql://\w+@[-\.\w]+:\d+/.+$', content['connection_string']))

        # Patch schema
        response = self.client.patch(
            reverse(
                viewname='schema-detail',
                args={content["schema_id"]},
            ),
            data={"access_key": access_key, "secret_key": secret_key, "unit": "13029"},
            format='json'
        )
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        self.assertEqual(content["unit"], "13029")

        sleep(10)

        # Clean stacks
        conn = rancher.Rancher()
        conn.clean_stacks(KERMIT_SCIPER)

    @tag('rancher')
    def test_get_schemas(self):
        """ Test the GET method of schemas"""

        # create an API key
        response = self.client.post(
            reverse('apikey-list'),
            data={"username": get_config('TEST_USERNAME'), "password": get_config('TEST_CORRECT_PWD')},
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.client.post(
            reverse('schema-list'),
            data={"access_key": content["access_key"],
                  "secret_key": content["secret_key"]},
            format='json'
        )

        response = self.client.get(
            reverse('schema-list'),
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
            reverse('version-detail'),
            format='json'
        )
        content = json.loads(response.content.decode('utf-8'))

        self.assertIsNotNone(re.match('^\d+\.\d+\.\d+$', content))
