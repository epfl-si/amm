"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^apikeys/$', views.keys, name="apikeys"),
    url(r'^schemas/$', views.schemas, name="schemas"),
]
