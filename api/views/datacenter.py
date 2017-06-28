from api.libs.base import CoreView
from cmdb.models import DataCenter
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


class DataCenterView(CoreView):
    login_required_action = ["get_list"]

    def get_list(self):
        per_page = self.parameters("per_page")
        if per_page:
            datacenter_objs = self.page_split(DataCenter.objects.all())
        else:
            datacenter_objs = DataCenter.objects.all()

        datacenter_list = []
        for datacenter_obj in datacenter_objs:
            datacenter_list.append(datacenter_obj.get_info())
        print(datacenter_list)
        self.response_data['data'] = datacenter_list