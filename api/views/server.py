from django.shortcuts import render

# Create your views here.
from api.libs.base import CoreView
from cmdb.models import Asset, BusinessUnit, Cabinet, Tags
from django.db.models import Q
from api.libs.cmdb_agent import CmdbCollector
from api.libs.asset_handler import AssetHandler
from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.models import User
from account.models import UserProfile


class Server(CoreView):
    login_required_action = ["get_list"]

    # permission_view_map = {
    #     "get_list": "can_view_asset"
    # }
    # app_name = "cmdb"

    def get_list(self):
        search = self.parameters('search')
        if not search:
            server_objs = self.page_split(Asset.objects.filter(
                business_unit__in=get_objects_for_user(self.request.user, "cmdb.view_project_asset")).all())
        else:
            server_objs = self.page_split(Asset.objects.filter(
                business_unit__in=get_objects_for_user(self.request.user, "cmdb.view_project_asset"))
                                          .filter(Q(name__contains=search) | Q(nics__ip_address__contains=search) |
                                                  Q(asset_num__contains=search)).distinct())
        server_list = []
        for server_obj in server_objs:
            server_list.append(server_obj.get_base_info())
        self.response_data['data'] = server_list

    def post_create(self):
        response_data = []
        username = self.parameters('username')
        password = self.parameters('password')
        project_id = self.parameters('project')
        ipaddresses = self.parameters('ipaddresses').split(';')
        port = self.parameters('port')
        for ipaddress in ipaddresses:
            cmdb_collector = CmdbCollector(host=ipaddress, username=username, password=password, ssh_port=port)
            cmdb_collector.collector_all()
            if cmdb_collector.msg:
                if "Failed to connect to the host via ssh" in cmdb_collector.msg:
                    response_data.append({"ipaddress": ipaddress, "status": False, "msg": "连接主机失败，请检查网络"})
                elif "Authentication failure" in cmdb_collector.msg:
                    response_data.append({"ipaddress": ipaddress, "status": False, "msg": "认证失败，请检查用户名密码是否正确"})
            else:
                if not Asset.objects.filter(
                        sn=cmdb_collector.asset_info.get('essential_information').get("SN")).first():
                    handler = AssetHandler(self.request, cmdb_collector.asset_info, project_id=project_id,
                                           management_ip=ipaddress)
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
                if self.request.user.has_perm('view_project_asset', asset_obj.business_unit):
                    self.response_data["data"] = asset_obj.get_info()
                    print(asset_obj.get_info().get("base").get("status"))
                else:
                    self.get_not_permission()
            else:
                self.response_data['status'] = False
                self.response_data['info'] = "asset id is not exit or invalid!"
        else:
            self.response_data['status'] = False
            self.response_data['info'] = "asset id is not exit or invalid!"

    def post_delete(self):
        asset_id = self.parameters("server_id")
        try:
            asset_obj = Asset.objects.filter(id=asset_id).first()
            asset_obj.delete()
        except Exception as e:
            self.response_data['status'] = False
            self.status_code = 500

    def post_change(self):
        asset_id = self.parameters("id")
        filed_name = self.parameters("filed_name")
        value = self.parameters("new_value")
        if value == "":
            value = None
        asset_obj = Asset.objects.filter(id=asset_id).first()
        if asset_obj:
            filed_name = filed_name.split(".")
            if filed_name[0] == 'base':
                if filed_name[1] not in ["admin", "raid_type", "cabinet", "business_unit", "operation", "tags"]:
                    setattr(asset_obj, filed_name[1], value)
                    asset_obj.save()
                if filed_name[1] == "cabinet":
                    cabinet_obj = Cabinet.objects.filter(id=value).first()
                    asset_obj.cabinet = cabinet_obj
                    asset_obj.save()
                if filed_name[1] == "business_unit":
                    business_unit_obj = BusinessUnit.objects.filter(id=value).first()
                    asset_obj.business_unit = business_unit_obj
                    asset_obj.save()
                if filed_name[1] == "admin":
                    admin_obj = UserProfile.objects.filter(id=value).first()
                    if admin_obj:
                        asset_obj.admin = admin_obj.user
                        asset_obj.save()
                    else:
                        asset_obj.admin = None
                        asset_obj.save()
                if filed_name[1] == "operation":
                    operation_obj = UserProfile.objects.filter(id=value).first()
                    if operation_obj:
                        asset_obj.operation = operation_obj.user
                        asset_obj.save()
                    else:
                        asset_obj.operation = None
                        asset_obj.save()
                if filed_name[1] == "tags":
                    asset_obj.tags = []
                    if value:
                        tags_list = value.split(",")
                        for tag in tags_list:
                            tag_obj = Tags.objects.filter(name=tag).first()
                            if tag_obj:
                                asset_obj.tags.add(tag_obj)
                            else:
                                tag_obj = Tags(name=tag)
                                tag_obj.save()
                                asset_obj.tags.add(tag_obj)
                    asset_obj.save()

            if filed_name[0] == 'server':
                setattr(asset_obj.server, filed_name[1], value)
                asset_obj.server.save()


        else:
            self.response_data['status'] = False
            self.status_code = 404
