import json

from django.urls import reverse
from rest_framework.test import APITestCase

from api.redis import flushall
from config.settings.base import get_config

import re


class KeyViewTestCase(APITestCase):

    def test_post_apikeys(self):
        """ Test the post method of KeyView """

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
        flushall(self)

    def test_get_apikeys(self):
        """ Test the post method of KeyView """

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
        flushall(self)

    def test_post_schemas(self):
        """ Test the post method of Schemas """

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

        self.assertIsNotNone(re.match('^mysql://\w+:[-\+\w]+@(\w\.?)+:\d+/.+$', content))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        flushall(self)

    
    def test_get_schemas(self):
        """ Test the GET method of schemas"""

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
        
        self.assertEqual(len(content), 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        flushall(self)
