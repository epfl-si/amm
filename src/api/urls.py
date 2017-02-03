from django.conf.urls import url
from api.views import key_list


urlpatterns = [
    url(r'^keys/$', key_list),

]
