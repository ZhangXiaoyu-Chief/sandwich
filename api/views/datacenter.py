from api.libs.base import CoreView
from cmdb.models import DataCenter
from django.contrib.auth.models import User
from account.models import UserProfile
from django.db.utils import IntegrityError


class DataCenterView(CoreView):
    """
    数据中心视图类
    """
    login_required_action = ["get_list", "post_create", "post_delete", "post_change"]
    superuser_required_action = ["post_create", "post_delete", "post_change"]

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
            address = self.parameters("address")
            admin_id = int(self.parameters("admin"))
            admin_obj = UserProfile.objects.filter(id=admin_id).first()
            if admin_obj and admin_obj.user:
                new_datacenter_obj = DataCenter(name=name, contact=contact, memo=memo, admin=admin_obj.user, address=address)
            else:
                new_datacenter_obj = DataCenter(name=name, contact=contact, memo=memo, address=address)
            new_datacenter_obj.save()
            self.response_data['data'] = new_datacenter_obj.get_info()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416
        except Exception:
            self.response_data['status'] = False
            self.status_code = 500

    def post_delete(self):
        datacenter_id = self.parameters("id")
        try:
            datacenter_obj = DataCenter.objects.filter(id=datacenter_id).first()
            if datacenter_obj:
                datacenter_obj.delete()
            else:
                self.response_data['status'] = False
                self.status_code = 404
        except Exception as e:
            self.response_data['status'] = False
            self.status_code = 500

    def post_change(self):
        datacenter_id = self.parameters("id")
        name = self.parameters("name")
        admin_id = self.parameters("admin_id")
        contact = self.parameters("contact")
        memo = self.parameters("memo")
        address = self.parameters("address")

        try:
            datacenter_obj = DataCenter.objects.filter(id=datacenter_id).first()
            if datacenter_obj:
                datacenter_obj.name = name
                admin_obj = UserProfile.objects.filter(id=admin_id).first()
                datacenter_obj.admin = admin_obj.user if admin_obj and hasattr(admin_obj, "user") else None
                datacenter_obj.contact = contact
                datacenter_obj.memo = memo
                datacenter_obj.address = address
                datacenter_obj.save()
                self.response_data['data'] = datacenter_obj.get_info()
            else:
                self.response_data['status'] = False
                self.status_code = 404
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416
        except Exception as e:
            self.response_data['status'] = False
            self.status_code = 500
