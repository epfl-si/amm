"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.conf.urls import url
from api import views
import auth

app = views.AMMApp(auth.get_configured_authenticator())

urlpatterns = [
    url(r'^apikeys/$', app.keys, name="apikeys"),
    url(r'^schemas/$', app.schemas, name="schemas"),
    url(r'^version/$', app.version, name='version'),
]
