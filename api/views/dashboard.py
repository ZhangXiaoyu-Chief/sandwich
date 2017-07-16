from api.libs.base import CoreView
from cmdb.models import Asset, BusinessUnit
from django.db.models import Sum, Count


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
