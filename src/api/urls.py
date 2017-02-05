from django.conf.urls import url
from api.views import key_list


urlpatterns = [
    url(r'^apikeys/$', key_list),

]
