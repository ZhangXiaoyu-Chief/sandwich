from api.libs.base import CoreView
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
from cmdb.models import BusinessUnit
from guardian.shortcuts import get_perms
import json
from guardian.shortcuts import assign_perm, remove_perm


class GroupView(CoreView):
    """
    用户组相关接口
    """

    login_required_action = ["get_list", "post_create", "post_change", "post_delete", "post_change_permissions"]
    superuser_required_action = ["get_list", "post_create", "post_change", "post_delete", "post_change_permissions"]

    def get_list(self):
        """
        获取用户组列表接口
        :return: 
        """
        group_list = []
        group_objs = Group.objects.all()
        for group_obj in group_objs:
            project_objs = BusinessUnit.objects.all()
            permissions = []
            for project_obj in project_objs:
                permissions.append({
                    "project_id":project_obj.id,
                    "project_name": project_obj.name,
                    "view_project_asset": "view_project_asset" in get_perms(group_obj, project_obj),
                    "add_project_asset": "add_project_asset" in get_perms(group_obj, project_obj),
                    "change_project_asset": "change_project_asset" in get_perms(group_obj, project_obj),
                    "del_project_asset": "del_project_asset" in get_perms(group_obj, project_obj)
                })
            group_list.append({
                "id": group_obj.id,
                "name": group_obj.name,
                "permissions":permissions
            })
        self.response_data['data'] = group_list

    def post_create(self):
        try:
            name = self.parameters("name")
            group_obj = Group(name=name)
            group_obj.save()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416

    def post_change(self):
        try:
            group_id = self.parameters("id")
            name = self.parameters("name")
            group_obj = Group.objects.filter(id=group_id).first()
            if group_obj:
                group_obj.name = name
                group_obj.save()

                self.response_data['data'] = {
                    "id": group_obj.id,
                    "name": group_obj.name
                }
            else:
                self.response_data['status'] = False
                self.status_code = 404
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416

    def post_delete(self):
        group_id = self.parameters("id")
        group_obj = Group.objects.filter(id=group_id).first()
        if group_obj:
            group_obj.delete()
        else:
            self.response_data['status'] = False
            self.status_code = 404

    def post_change_permissions(self):
        permissions = json.loads(self.parameters("permissions"))
        group_id = self.parameters("id")
        group_obj = Group.objects.filter(id = group_id).first()
        if group_obj:
            for permission in permissions:
                project_obj = BusinessUnit.objects.filter(id=permission.get("project_id")).first()
                if project_obj:
                    if permission.get("view_project_asset"):
                        assign_perm("view_project_asset", group_obj, project_obj)
                    else:
                        remove_perm("view_project_asset", group_obj, project_obj)
                    if permission.get("add_project_asset"):
                        assign_perm("add_project_asset", group_obj, project_obj)
                    else:
                        remove_perm("add_project_asset", group_obj, project_obj)
                    if permission.get("change_project_asset"):
                        assign_perm("change_project_asset", group_obj, project_obj)
                    else:
                        remove_perm("change_project_asset", group_obj, project_obj)
                    if permission.get("del_project_asset"):
                        assign_perm("del_project_asset", group_obj, project_obj)
                    else:
                        remove_perm("del_project_asset", group_obj, project_obj)
        else:
            self.response_data['status'] = False
            self.status_code = 404



