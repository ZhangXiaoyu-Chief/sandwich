from django.shortcuts import render

# Create your views here.
from api.libs.base import CoreView
from cmdb.models import Asset


class Server(CoreView):
    def get_list(self):
        server_objs = self.page_split(Asset.objects.filter(asset_type='server').all())
        server_list = []
        for server_obj in server_objs:
            server_list.append(server_obj.get_base_info())
        self.response_data['data'] = server_list