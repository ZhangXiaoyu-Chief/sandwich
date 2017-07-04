from api.libs.base import CoreView
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError


class GroupView(CoreView):
    """
    用户组相关接口
    """
    def get_list(self):
        """
        获取用户组列表接口
        :return: 
        """
        group_list = []
        group_objs = Group.objects.all()
        for group_obj in group_objs:
            group_list.append({
                "id": group_obj.id,
                "name": group_obj.name
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
