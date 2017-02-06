from django.conf.urls import url
from api.views import keys


urlpatterns = [
    url(r'^apikeys/$', keys),

]
