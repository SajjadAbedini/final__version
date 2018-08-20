from app1.api.views import request_api
from django.conf.urls import url
urlpatterns = [
    url(r'^request/$',request_api.as_view(),name="api_list"),
]
