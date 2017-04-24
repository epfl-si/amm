"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf.urls import url, include

from api import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^v1/', include('api.urls')),
]
