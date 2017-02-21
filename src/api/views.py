"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import django.http
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api import utils
from config.settings import base


class AMMApp(object):
    def __init__(self, authenticator, apikey_handler, rancher):
        self.authenticator = authenticator
        self.apikey_handler = apikey_handler
        self.rancher = rancher

    def generate_response(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        return django.http.HttpResponse(content, **kwargs)

    @csrf_exempt
    def keys(self, request):
        """ View to manage """

        if request.method == 'GET':

            username = self.apikey_handler.validate(
                                            request.GET.get('access_key', None),
                                            request.GET.get('secret_key', None)
                                          )
            if username is not None:
                keys = self.apikey_handler.get_keys(username)
                return self.generate_response(keys, status=200)

            return self.generate_response("Invalid APIKeys", status=403)

        if request.method == 'POST':

            data = JSONParser().parse(request)

            if self.authenticator.authenticate(data['username'], data['password']):
                thekey = self.apikey_handler.generate_keys(data['username'])
                return self.generate_response(thekey.get_values(), status=200)
            else:
                return self.generate_response("Authentication Failed", status=401)

        return self.generate_response("Expecting GET or POST method", status=400)

    @csrf_exempt
    def schemas(self, request):
        """ View to manage """

        if request.method == 'GET':
            username = self.apikey_handler.validate(
                                            request.GET.get('access_key', None),
                                            request.GET.get('secret_key', None)
                                          )
            if username is not None:
                stacks = self.rancher.get_stacks(username)
                return self.generate_response(stacks, status=200)

            return self.generate_response("Invalid APIKeys", status=403)

        if request.method == 'POST':

            data = JSONParser().parse(request)

            username = self.apikey_handler.validate(
                                            data.get('access_key', None),
                                            data.get('secret_key', None)
                                          )
            if username is not None:
                db_username = utils.generate_random_b64(10)
                db_password = utils.generate_password(32)
                db_port = 1234
                db_schema = utils.generate_random_b64(10)
                db_stack = utils.generate_random_b64(20)
                db_env = base.get_config('AMM_ENVIRONMENT')

                self.rancher.create_stack(username, db_username, db_password, db_port, db_schema, db_stack, db_env)

                connection = "mysql://%s:%s@mysql.%s.%s.epfl.ch:%s/%s" % (db_username, db_password, db_stack,
                                                                          db_env, db_port, db_schema)

                return self.generate_response(connection, status=200)

            return self.generate_response("Invalid APIKeys", status=403)

        return self.generate_response("Bad request", status=400)

    @csrf_exempt
    def version(self, request):
        """ View to get version number """
        return self.generate_response(base.VERSION, status=200)
