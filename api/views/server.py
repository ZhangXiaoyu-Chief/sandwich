from django.shortcuts import render

# Create your views here.
from api.libs.base import CoreView
from cmdb.models import Asset
from django.db.models import Q
from api.libs.cmdb_agent import CmdbCollector
from api.libs.asset_handler import AssetHandler


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

    def post_create(self):
        response_data = []
        username = self.parameters('username')
        password = self.parameters('password')
        ipaddresses = self.parameters('ipaddresses').split(';')
        port = self.parameters('port')
        for ipaddress in ipaddresses:
            cmdb_collector = CmdbCollector(host=ipaddress, username=username, password=password, ssh_port=port)
            cmdb_collector.collector_all()
            if cmdb_collector.msg:
                if "Failed to connect to the host via ssh" in cmdb_collector.msg:
                    response_data.append({"ipaddress":ipaddress, "status": False, "msg": "连接主机失败，请检查网络"})
                elif "Authentication failure" in cmdb_collector.msg:
                    response_data.append({"ipaddress":ipaddress, "status": False, "msg": "认证失败，请检查用户名密码是否正确"})
            else:
                if not Asset.objects.filter(sn = cmdb_collector.asset_info.get('essential_information').get("SN")).first():
                    handler = AssetHandler(self.request, cmdb_collector.asset_info)
                    handler.create_asset('server')
                    response_data.append({"ipaddress": ipaddress, "status": True, "msg": "添加成功"})
                else:
                    response_data.append({"ipaddress": ipaddress, "status": False, "msg": "此服务器已经存在"})
        self.response_data['data'] = response_data

    def get_detail(self):
        asset_id = self.parameters("id")
        if asset_id:
            asset_obj = Asset.objects.filter(id=asset_id).first()
            if asset_obj:
                self.response_data["data"] = asset_obj.get_info()
            else:
                self.response_data['status'] = False
                self.response_data['msg'] = "asset id is not exit or invalid!"
        else:
            self.response_data['status'] = False
            self.response_data['msg'] = "asset id is not exit or invalid!"
