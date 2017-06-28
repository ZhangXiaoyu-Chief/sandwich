from django.conf.urls import include, url
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^server/(?P<action>\w+)/$', csrf_exempt(views.Server.as_view())),
    url(r'^account/(?P<action>\w+)/$', csrf_exempt(views.Account.as_view())),
    url(r'^upload/(?P<action>\w+)/$', csrf_exempt(views.Upload.as_view())),
    url(r'^project/(?P<action>\w+)/$', csrf_exempt(views.Project.as_view())),
    url(r'^datacenter/(?P<action>\w+)/$', csrf_exempt(views.DataCenter.as_view())),
]