"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.conf.urls import url
from api import views


urlpatterns = [
    url(r'^apikeys/$', views.KeysView.as_view(), name="apikeys"),
    url(r'^schemas/$', views.SchemasView.as_view(), name="schemas"),
    url(r'^version/$', views.VersionView.as_view(), name='version'),
]
