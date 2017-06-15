from django.conf.urls import url,include
from cmdb import views

urlpatterns = [
    url(r'server_list/', views.get_server_list, name='server_list'),  # 资产列表
]