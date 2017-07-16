from django.shortcuts import render

# Create your views here.
from api.libs.base import CoreView
from cmdb.models import Asset, BusinessUnit, Cabinet, Tags, EventLog
from django.db.models import Q
from api.libs.cmdb_agent import CmdbCollector
from api.libs.asset_handler import AssetHandler
from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.models import User
from account.models import UserProfile
from django.conf import settings


class Server(CoreView):
    login_required_action = ["get_list", "post_create", "get_detail", "post_delete", "post_change"]

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
        project_obj = BusinessUnit.objects.filter(id=project_id).first()
        if not project_obj or not self.request.user.has_perm('add_project_asset', project_obj):
            self.response_data["status"] = False
            self.status_code = 403
            return
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
        asset_obj = Asset.objects.filter(id=asset_id).first()
        if asset_obj:
            if self.request.user.has_perm("del_project_asset", asset_obj.business_unit):
                asset_obj.delete()
            else:
                self.response_data['status'] = False
                self.status_code = 403
        else:
            self.response_data['status'] = False
            self.status_code = 404

    def post_change(self):
        asset_id = self.parameters("id")
        filed_name = self.parameters("filed_name")
        value = self.parameters("new_value")
        if value == "":
            value = None
        asset_obj = Asset.objects.filter(id=asset_id).first()
        filed_name_map = {
            "asset_num": "资产编号",
            "status": "运营状态",
            "management_ip": "管理IP",
            "raid_type": "Raid类型",
            "price": "价格",
            "trade_date": "购买时间",
            "expire_date": "过保时间",
            "cabinet": "机柜",
            "admin": "负责人",
            "operation": "运维人员",
            "business_unit": "所属项目",
        }
        status_map = dict()
        for status_item in settings.ASSET_STATUS_CHOICES:
            status_map[status_item[0]] = status_item[1]
        if asset_obj:
            if not self.request.user.has_perm("change_project_asset", asset_obj.business_unit):
                self.response_data["status"] = False
                self.status_code = 403
                return
            filed_name = filed_name.split(".")
            old_value = None
            new_value = None

            if filed_name[0] == 'base':
                if filed_name[1] not in ["admin", "raid_type", "cabinet", "business_unit", "operation", "tags"]:
                    old_value = getattr(asset_obj, filed_name[1])
                    if not value == old_value:
                        setattr(asset_obj, filed_name[1], value)
                        asset_obj.save()
                        if filed_name[1] == "status":
                            old_value = status_map[old_value]
                            new_value = status_map[int(value)]
                        else:
                            new_value = value
                if filed_name[1] == "cabinet":
                    old_value = asset_obj.cabinet.number if asset_obj.cabinet else "空"
                    cabinet_obj = Cabinet.objects.filter(id=value).first()
                    new_value = cabinet_obj.number if cabinet_obj else "空"
                    if not old_value == new_value:
                        asset_obj.cabinet = cabinet_obj
                        asset_obj.save()
                if filed_name[1] == "business_unit":
                    old_value = asset_obj.business_unit.name if asset_obj.business_unit else "空"
                    business_unit_obj = BusinessUnit.objects.filter(id=value).first()
                    new_value = business_unit_obj.name if business_unit_obj else "空"
                    if not old_value == new_value:
                        asset_obj.business_unit = business_unit_obj
                        asset_obj.save()
                if filed_name[1] == "admin":
                    old_value = asset_obj.admin.username if asset_obj.admin else "空"
                    admin_obj = UserProfile.objects.filter(id=value).first()
                    new_value = admin_obj.user.username if admin_obj and admin_obj.user else "空"
                    if not old_value == new_value:
                        asset_obj.admin = admin_obj.user if admin_obj else None
                        asset_obj.save()

                if filed_name[1] == "operation":
                    old_value = asset_obj.operation.username if asset_obj.operation else "空"
                    operation_obj = UserProfile.objects.filter(id=value).first()
                    new_value = operation_obj.user.username if operation_obj and operation_obj.user else "空"
                    if not old_value == new_value:
                        asset_obj.operation = operation_obj.user if operation_obj else None
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

            if new_value or not old_value:
                msg = "变更%s：旧配置：%s 新配置：%s" % (filed_name_map[filed_name[1]], old_value, new_value)
                log_obj = EventLog(asset=asset_obj,
                                   event_type=1,
                                   operater=self.request.user,
                                   component=None,
                                   detail=msg
                                   )
                log_obj.save()
        else:
            self.response_data['status'] = False
            self.status_code = 404
