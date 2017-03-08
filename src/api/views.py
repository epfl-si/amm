"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import django.http
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api.utils import get_sciper
from config.settings import base


class AMMApp(object):
    def __init__(self, authenticator, apikey_handler, rancher):
        self.authenticator = authenticator
        self.apikey_handler = apikey_handler
        self.rancher = rancher

    def generate_response(self, data, **kwargs):
        """generate the JSON response"""

        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        return django.http.HttpResponse(content, **kwargs)

    @csrf_exempt
    def keys(self, request):
        """ API for managing the keys """

        # with GET we return the user's keys
        if request.method == 'GET':

            # first we check the key
            username = self.apikey_handler.validate(
                                            request.GET.get('access_key', None),
                                            request.GET.get('secret_key', None)
                                          )
            if username is not None:
                keys = self.apikey_handler.get_keys(username)
                return self.generate_response(keys, status=200)

            return self.generate_response("Invalid APIKey", status=403)

        # with POST we create a new key
        if request.method == 'POST':

            data = JSONParser().parse(request)

            if self.authenticator.authenticate(data['username'], data['password']):
                thekey = self.apikey_handler.generate_keys(data['username'])
                return self.generate_response(thekey.get_values(), status=200)
            else:
                return self.generate_response("Authentication failed", status=401)

        return self.generate_response("Expecting GET or POST method", status=400)

    @csrf_exempt
    def schemas(self, request):
        """ API for managing schemas """

        # with GET we return the user's schemas
        if request.method == 'GET':
            username = self.apikey_handler.validate(
                                            request.GET.get('access_key', None),
                                            request.GET.get('secret_key', None)
                                          )
            if username:
                sciper = get_sciper(username)
                stacks = self.rancher.get_schemas(sciper)
                return self.generate_response(stacks, status=200)

            return self.generate_response("Invalid APIKey", status=403)

        # with POST we create a new schema
        if request.method == 'POST':

            data = JSONParser().parse(request)

            username = self.apikey_handler.validate(
                                            data.get('access_key', None),
                                            data.get('secret_key', None)
                                          )
            if username:
                response = {}

                sciper = get_sciper(username)

                data = self.rancher.create_mysql_stack(sciper)
                response["connection_string"] = data["connection_string"]
                response["mysql_cmd"] = data["mysql_cmd"]

                return self.generate_response(response, status=200)

            return self.generate_response("Invalid APIKeys", status=403)

        return self.generate_response("Expecting GET or POST method", status=400)

    @csrf_exempt
    def version(self, request):
        """ Return the API version number """
        if request.method == 'GET':
            return self.generate_response(base.VERSION, status=200)
        return self.generate_response("Expecting GET method", status=400)
