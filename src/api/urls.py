"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.conf.urls import url
from api import views, rancher, apikeyhandler
import auth

rancher_api = rancher.Rancher()
apikey_handler = apikeyhandler.ApiKeyHandler()
authenticator = auth.get_configured_authenticator()

ammapp = views.AMMApp(authenticator, apikey_handler, rancher_api)

urlpatterns = [
    url(r'^apikeys/$', ammapp.keys, name="apikeys"),
    url(r'^schemas/$', ammapp.schemas, name="schemas"),
    url(r'^version/$', ammapp.version, name='version'),
]
