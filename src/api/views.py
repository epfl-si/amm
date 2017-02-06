"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from api.models import APIKey
from api.redis import save_key, exists, get_apikeys


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):

        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def ldap_authentificate(username, password):
    """
    LDAPs authentication
    """

    # connection = get_ldap_connection(username, password)
    connection = True
    if connection:
        return username
    return False


@csrf_exempt
def keys(request):
    """ View to manage """

    if request.method == 'GET':

        data = JSONParser().parse(request)

        username = exists(data['access_key'], data['secret_key'])
        if username:
            apikeys = get_apikeys(username=username)
            return JSONResponse(apikeys, status=201)

        return JSONResponse("APIKey doesn't exist", status=403)

    if request.method == 'POST':

        data = JSONParser().parse(request)
        username = ldap_authentificate(data['username'], data['password'])

        if username:
            apikey = APIKey()
            save_key(username, apikey)
            dict = apikey.__dict__
            return JSONResponse(dict, status=201)
        return JSONResponse("Ldaps authentication failed", status=400)
