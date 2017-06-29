from api.libs.base import CoreView
from cmdb.models import DataCenter
from django.contrib.auth.models import User
from account.models import UserProfile
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
        self.response_data['data'] = datacenter_list

    def post_create(self):
        try:
            name = self.parameters("name")
            contact = self.parameters("contact")
            memo = self.parameters("memo")
            admin_id = int(self.parameters("admin"))
            admin_obj = UserProfile.objects.filter(id=admin_id).first()
            if admin_obj and admin_obj.user:
                new_datacenter_obj = DataCenter(name=name, contact=contact, memo=memo, admin=admin_obj.user)
            else:
                new_datacenter_obj = DataCenter(name=name, contact=contact, memo=memo)
            new_datacenter_obj.save()
            self.response_data['data'] = new_datacenter_obj.save()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416
        except Exception:
            self.response_data['status'] = False
            self.status_code = 500