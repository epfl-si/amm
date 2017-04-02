"""(c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017"""

from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^units/$', views.UnitList.as_view(), name="unit-list"),
    url(r'^units/(?P<unit_id>[^/.]+)/$', views.UnitDetail.as_view(), name="unit-detail"),
    url(r'^units/(?P<unit_id>[^/.]+)/schemas/$', views.SchemaListByUnit.as_view(), name="schema-list-by-unit"),

    url(r'^apikeys/$', views.APIKeyList.as_view(), name="apikey-list"),

    url(r'^users/$', views.UserList.as_view(), name="user-list"),
    url(r'^users/(?P<user_id>[^/.]+)/$', views.UserDetail.as_view(), name="user-detail"),
    url(r'^users/(?P<user_id>[^/.]+)/schemas/$', views.SchemaListByUser.as_view(), name="schema-list-by-user"),

    url(r'^schemas/$', views.SchemaList.as_view(), name="schema-list"),
    url(r'^schemas/(?P<schema_id>[^/.]+)/$', views.SchemaDetail.as_view(), name="schema-detail"),

    url(r'^version/$', views.VersionDetail.as_view(), name='version-detail'),
]
