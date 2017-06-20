from django.shortcuts import render

# Create your views here.
from api.libs.base import CoreView
from cmdb.models import Asset
from django.db.models import Q

class Server(CoreView):
    def get_list(self):
        search = self.parameters('search')
        if not search:
            server_objs = self.page_split(Asset.objects.filter(asset_type='server').all())
        else:
            server_objs = self.page_split(Asset.objects.filter(asset_type='server').filter(Q(name__contains=search) | Q(nics__ip_address__contains=search) | Q(asset_num__contains=search)))
        server_list = []
        for server_obj in server_objs:
            server_list.append(server_obj.get_base_info())
        self.response_data['data'] = server_list
