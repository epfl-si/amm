"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^v1/', include('api.urls')),
    url(r'^admin/', admin.site.urls),

]
