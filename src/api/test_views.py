import json

from django.urls import reverse
from rest_framework.test import APITestCase

from api.redis import flushall
from config.settings.base import get_secret


class KeyViewTestCase(APITestCase):

    def test_post(self):
        """ Test the post method of KeyView """

        response = self.client.post(
            reverse('apikeys'),
            data={"username": "kermit", "password": get_secret("TEST_PWD")},
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(len(content["access_key"]), 20)
        self.assertEqual(len(content["secret_key"]), 40)

        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        flushall(self)

    def test_get(self):
        """ Test the post method of KeyView """

        response = self.client.post(
            reverse('apikeys'),
            data={"username": "kermit", "password": get_secret("TEST_PWD")},
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

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response['content-type'],
            'application/json'
        )
        flushall(self)
