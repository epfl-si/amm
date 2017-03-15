"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

from api import views

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    # url(r'^$', schema_view),
    url(r'^$', views.api_root),
    url(r'^v1/', include('api.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
