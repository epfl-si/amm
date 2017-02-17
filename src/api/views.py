"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api import apikey, redis, utils, rancher


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):

        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def keys(request):
    """ View to manage """

    if request.method == 'GET':

        if 'access_key' in request.GET and 'secret_key' in request.GET:
            username = redis.exists(request.GET['access_key'], request.GET['secret_key'])
            if username:
                apikeys = redis.get_apikeys(username=username)
                return JSONResponse(apikeys, status=200)

            return JSONResponse("APIKey doesn't exist", status=403)

    if request.method == 'POST':

        data = JSONParser().parse(request)

        if utils.authenticate(data['username'], data['password']):
            thekey = apikey.APIKey.generate()
            redis.save_key(data['username'], thekey)
            return JSONResponse(thekey.get_values(), status=200)
        else:
            return JSONResponse("Ldaps authentication failed", status=401)

    return JSONResponse("Bad request", status=400)

@csrf_exempt
def connections(request):
    """ View to manage """

    if request.method == 'GET':
        if 'access_key' in request.GET and 'secret_key' in request.GET:
            username = redis.exists(request.GET['access_key'], request.GET['secret_key'])
            if username:
                return JSONResponse(rancher.get_stacks(username), status=200)

            return JSONResponse("APIKey doesn't exist", status=403)

        return JSONResponse("Bad request", status=400)

    if request.method == 'POST':

        if 'access_key' in request.GET and 'secret_key' in request.GET:
            username = redis.exists(request.GET['access_key'], request.GET['secret_key'])
            if username:
                db_username = utils.generate_random_b64(10)
                db_password = utils.generate_password(32)
                db_port = 1234
                db_schema = utils.generate_random_b64(10)
                db_stack = utils.generate_random_b64(20)
                db_env = utils.get_config('AMM_ENVIRONMENT')

                rancher.create_stack(username, db_username, db_password, db_port, db_schema, db_stack, db_env)

                connection = "mysql://%s:%s@mysql.%s.%s.epfl.ch:%s/%s" % (db_username, db_password, db_stack, db_env,
                                                                          db_port, db_schema)

                return JSONResponse(connection, status=200)

            return JSONResponse("APIKey doesn't exist", status=403)

    return JSONResponse("Bad request", status=400)