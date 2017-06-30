from api.libs.base import CoreView
from cmdb.models import MachineRoom
from account.models import UserProfile


class MachineRoomView(CoreView):
    """
    机房视图类
    """
    def get_list(self):
        per_page = self.parameters("per_page")
        if per_page:
            machineroom_objs = self.page_split(MachineRoom.objects.all())
        else:
            machineroom_objs = MachineRoom.objects.all()

        machineroom_list = []
        for machineroom_obj in machineroom_objs:
            machineroom_list.append(machineroom_obj.get_info())
        self.response_data["data"] = machineroom_list