"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from api.apikey import APIKey
from api.redis import save_key, exists, get_apikeys
from api.utils import authenticate


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
            username = exists(request.GET['access_key'], request.GET['secret_key'])
            if username:
                apikeys = get_apikeys(username=username)
                return JSONResponse(apikeys, status=200)

            return JSONResponse("APIKey doesn't exist", status=403)

    if request.method == 'POST':

        data = JSONParser().parse(request)

        if authenticate(data['username'], data['password']):
            apikey = APIKey.generate()
            save_key(data['username'], apikey)
            return JSONResponse(apikey.get_values(), status=200)
        else:
            return JSONResponse("Ldaps authentication failed", status=401)

    return JSONResponse("Bad request", status=400)
