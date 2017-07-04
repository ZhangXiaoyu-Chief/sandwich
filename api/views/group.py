from api.libs.base import CoreView
from django.contrib.auth.models import Group

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
