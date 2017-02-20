"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

import django.http
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api import apikey, redis, utils, rancher
from config.settings import base


class AMMApp(object):
    def __init__(self, authenticator):
        self.authenticator = authenticator

    def generate_response(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        return django.http.HttpResponse(content, **kwargs)

    @csrf_exempt
    def keys(self, request):
        """ View to manage """

        if request.method == 'GET':

            if 'access_key' in request.GET and 'secret_key' in request.GET:
                username = redis.exists(request.GET['access_key'], request.GET['secret_key'])
                if username:
                    apikeys = redis.get_apikeys(username=username)
                    return self.generate_response(apikeys, status=200)

                return self.generate_response("APIKey doesn't exist", status=403)

        if request.method == 'POST':

            data = JSONParser().parse(request)

            if self.authenticator.authenticate(data['username'], data['password']):
                thekey = apikey.APIKey.generate()
                redis.save_key(data['username'], thekey)
                return self.generate_response(thekey.get_values(), status=200)
            else:
                return self.generate_response("Authentication Failed", status=401)

        return self.generate_response("Expecting GET or POST method", status=400)

    @csrf_exempt
    def schemas(self, request):
        """ View to manage """

        r = rancher.Rancher()

        if request.method == 'GET':
            if 'access_key' in request.GET and 'secret_key' in request.GET:
                username = redis.exists(request.GET['access_key'], request.GET['secret_key'])
                if username:

                    return self.generate_response(r.get_stacks(username), status=200)

                return self.generate_response("APIKey doesn't exist", status=403)

            return self.generate_response("No api key given", status=400)

        if request.method == 'POST':

            data = JSONParser().parse(request)

            if 'access_key' in data and 'secret_key' in data:
                username = redis.exists(data['access_key'], data['secret_key'])
                if username:
                    db_username = utils.generate_random_b64(10)
                    db_password = utils.generate_password(32)
                    db_port = 1234
                    db_schema = utils.generate_random_b64(10)
                    db_stack = utils.generate_random_b64(20)
                    db_env = base.get_config('AMM_ENVIRONMENT')

                    r.create_stack(username, db_username, db_password, db_port, db_schema, db_stack, db_env)

                    connection = "mysql://%s:%s@mysql.%s.%s.epfl.ch:%s/%s" % (db_username, db_password, db_stack,
                                                                              db_env, db_port, db_schema)

                    return self.generate_response(connection, status=200)

                return self.generate_response("APIKey doesn't exist", status=403)

            return self.generate_response("No api key given", status=400)

        return self.generate_response("Bad request", status=400)

    @csrf_exempt
    def version(self, request):
        """ View to get version number """
        return self.generate_response(base.VERSION, status=200)
