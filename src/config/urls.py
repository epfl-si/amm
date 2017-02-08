"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf.urls import url, include


urlpatterns = [
    url(r'^v1/', include('api.urls')),
]
