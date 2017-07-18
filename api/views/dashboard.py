from api.libs.base import CoreView
from cmdb.models import Asset, BusinessUnit, Server, EventLog
from django.db.models import Sum, Count
from django.conf import settings
from account.models import UserProfile


class Dashboard(CoreView):
    login_required_action = []
    superuser_required_action = []

    def get_business_unit_count(self):
        business_unit_count = Asset.objects.values(
            'business_unit__name').annotate(Count('id'))
        legend = []
        data = []
        for business_unit in business_unit_count.all():
            legend.append(business_unit["business_unit__name"])
            data.append({
                "name": business_unit["business_unit__name"],
                "value": business_unit["id__count"]
            })

        self.response_data['data'] = {
            "legend": legend,
            "data": data
        }

    def get_os_relese_count(self):
        os_release_count = Asset.objects.values('server__os_release', 'server__os_type').annotate(Count('id'))
        legend = []
        data = []
        for os_release in os_release_count.all():
            legend.append("%s %s" % (os_release["server__os_type"], os_release["server__os_release"]))
            data.append({
                "name": "%s %s" % (os_release["server__os_type"], os_release["server__os_release"]),
                "value": os_release["id__count"]
            })

        self.response_data['data'] = {
            "legend": legend,
            "data": data
        }

    def get_status_count(self):
        status_count = Asset.objects.values('status').annotate(Count('id'))
        legend = []
        data = []
        status_map = dict()
        for status_item in settings.ASSET_STATUS_CHOICES:
            status_map[status_item[0]] = status_item[1]
        for status in status_count.all():
            legend.append(status_map.get(int(status["status"])))
            data.append({
                "name": status_map.get(int(status["status"])),
                "value": status["id__count"]
            })

        self.response_data['data'] = {
            "legend": legend,
            "data": data
        }

    def get_info(self):
        user_count = UserProfile.objects.count()
        server_count = Server.objects.count()
        project_count = BusinessUnit.objects.count()

        self.response_data['data'] = {
            "user_count": user_count,
            "server_count": server_count,
            "project_count": project_count,
        }

    def get_asset_log(self):
        log_objs = EventLog.objects.all().order_by("-date")
        logs = []
        for log_obj in log_objs[0:50]:
            logs.append(log_obj.get_info())

        self.response_data["data"] = logs
