from django.conf.urls import include, url
from api import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^server/(?P<action>\w+)/$', csrf_exempt(views.Server.as_view())),
    url(r'^account/(?P<action>\w+)/$', csrf_exempt(views.Account.as_view())),
    url(r'^upload/(?P<action>\w+)/$', csrf_exempt(views.Upload.as_view())),
    url(r'^project/(?P<action>\w+)/$', csrf_exempt(views.Project.as_view())),
    url(r'^datacenter/(?P<action>\w+)/$', csrf_exempt(views.DataCenter.as_view())),
    url(r'^machineroom/(?P<action>\w+)/$', csrf_exempt(views.MachineRoom.as_view())),
    url(r'^cabinet/(?P<action>\w+)/$', csrf_exempt(views.Cabinet.as_view())),
    url(r'^group/(?P<action>\w+)/$', csrf_exempt(views.Group.as_view())),
    url(r'^dashboard/(?P<action>\w+)/$', csrf_exempt(views.Dashboard.as_view())),
    url(r'^monitor/(?P<action>\w+)/$', csrf_exempt(views.Monitor.as_view())),
]
