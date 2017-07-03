from api.libs.base import CoreView
from cmdb.models import Cabinet, MachineRoom
from django.db.utils import IntegrityError


class CabinetView(CoreView):
    """
    机房视图类
    """
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
        print(self.request.POST)
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
        except Exception:
            self.response_data['status'] = False
            self.status_code = 500