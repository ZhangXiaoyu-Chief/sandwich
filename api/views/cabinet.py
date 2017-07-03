from api.libs.base import CoreView
from cmdb.models import Cabinet,MachineRoom
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