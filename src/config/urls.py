"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf.urls import url, include

from rest_framework_swagger.views import get_swagger_view

from api import views

schema_view = get_swagger_view(title='AMM API')

urlpatterns = [
    url(r'^$', views.api_root),
    # url(r'^docs/$', schema_view),
    url(r'^v1/', include('api.urls')),

]
