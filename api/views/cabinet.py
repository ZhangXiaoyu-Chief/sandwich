from api.libs.base import CoreView
from cmdb.models import Cabinet, MachineRoom
from django.db.utils import IntegrityError


class CabinetView(CoreView):
    """
    机房视图类
    """
    login_required_action = ["get_list", "post_create", "post_delete", "post_change"]
    superuser_required_action = ["post_create", "post_delete", "post_change"]

    def get_list(self):
        per_page = self.parameters("per_page")
        if per_page:
            cabinet_objs = self.page_split(Cabinet.objects.all())
        else:
            cabinet_objs = Cabinet.objects.all()
        cabinet_list = []
        for cabinet_obj in cabinet_objs:
            cabinet_list.append(cabinet_obj.get_info())
        self.response_data["data"] = cabinet_list

    def post_create(self):
        try:
            number = self.parameters("number")
            machineroom = self.parameters("machineroom")
            memo = self.parameters("memo")
            slotcount = self.parameters("slotcount")
            machineroom_obj = MachineRoom.objects.filter(id=machineroom).first()
            if machineroom_obj:
                new_cabinet_obj = Cabinet(number=number, slotcount=slotcount, memo=memo, room=machineroom_obj)
            else:
                new_cabinet_obj = Cabinet(number=number, slotcount=slotcount, memo=memo)
            new_cabinet_obj.save()
            self.response_data['data'] = new_cabinet_obj.get_info()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416

    def post_delete(self):
        cabinet_id = self.parameters("id")
        cabinet_obj = Cabinet.objects.filter(id=cabinet_id).first()
        if cabinet_obj:
            cabinet_obj.delete()
        else:
            self.response_data['status'] = False
            self.status_code = 404

    def post_change(self):
        try:
            number = self.parameters("number")
            cabinet_id = self.parameters("id")
            machineroom_id = self.parameters("machineroom_id")
            memo = self.parameters("memo")
            slotcount = self.parameters("slotcount")
            cabinet_obj = Cabinet.objects.filter(id=cabinet_id).first()
            if cabinet_obj:
                cabinet_obj.number = number
                machineroom_obj = MachineRoom.objects.filter(id=machineroom_id).first()
                cabinet_obj.room = machineroom_obj
                cabinet_obj.slotcount = slotcount
                cabinet_obj.memo = memo
                cabinet_obj.save()
                self.response_data['data'] = cabinet_obj.get_info()
            else:
                self.response_data['status'] = False
                self.status_code = 404
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416