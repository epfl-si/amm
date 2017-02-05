"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from api.models import Key
from api.redis import save_apikey_in_redis, is_exist


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):

        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def ldap_authentificate(username, password):

    # connection = get_ldap_connection()
    connection = True
    if connection:
        return username
    return False


@csrf_exempt
def key_list(request):

    if request.method == 'GET':

        data = JSONParser().parse(request)
        username = is_exist(data['apikey'])
        if username:
            apikeys = get_apikeys(username)
            username = str(username, 'utf-8')
            dict[username] = keys
        return JSONResponse(dict, status=201)

    if request.method == 'POST':

        data = JSONParser().parse(request)
        username = ldap_authentificate(data['username'], data['password'])

        if not username:
            LDAPS_AUTHENTIFICATION_ERROR = "Ldaps authentication failed"
        else:
            key = Key()
            save_apikey_in_redis(username, key.__str__())
            dict = key.__dict__
            dict['apikey'] = key.get_apikey()
            return JSONResponse(dict, status=201)
        return JSONResponse(LDAPS_AUTHENTIFICATION_ERROR, status=400)
