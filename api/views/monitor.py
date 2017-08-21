from api.libs.base import CoreView
from cmdb.models import Server
from monitor.libs.zabbix_api import ZabbixApi
import re
from monitor import settings
import json
import time

class Monitor(CoreView):
    login_required_action = [""]

    def get_graphs(self):
        url = settings.ZABBIX_SERVER.get("API_URL")
        username = settings.ZABBIX_SERVER.get("USERNAME")
        password = settings.ZABBIX_SERVER.get("PASSWORD")
        host_name = self.parameters("hostname")
        zabbix_obj = ZabbixApi(url=url, username=username, password=password)
        host_info = zabbix_obj.get_hosts_by_name(host_name)
        graph_list = []
        if host_name:
            host_info = host_info[1] if host_info[0] else {}
            if host_info and host_info[0]:
                host_id = host_info[0].get("hostid")
                graphs = zabbix_obj.get_graph_by_id(host_id)

                if graphs[0] and graphs[1]:
                    for graph in graphs[1]:
                        items = zabbix_obj.get_item_by_graph(graph.get("graphid"))
                        legend = []
                        series = []
                        unit = ""
                        x_axis =[]
                        _tmp_data = []
                        _max_data = 0
                        _max_item = ""
                        # if graph.get("graphtype") != "2":continue
                        if items[0] and items[1]:
                            for item in items[1]:
                                item_type = item.get("type")
                                item_obj = zabbix_obj.get_item_by_id(item["itemid"])[1][0]
                                unit = item_obj.get("unit") if item_obj.get("unit") else ""
                                history = item_obj["value_type"]
                                item_name = item_obj.get("name")
                                keys = re.search(r"\[([^\]]*)\]", item_obj.get("key_"))
                                keys = keys.groups()[0].split(",") if keys else ""

                                for _key in keys:
                                    item_name = item_name.replace("$%s" % (keys.index(_key) + 1), _key)

                                item_name = "%s 单位（%s）" % (item_name, item_obj.get("unit")) if item_obj.get(
                                    "unit") else item_name
                                legend.append(item_name)
                                if graph.get("graphtype") != "2":

                                    if item_type != 2:
                                        history_data = zabbix_obj.get_history_by_item(item_obj["itemid"], history)[1]
                                    else:
                                        history_data = zabbix_obj.get_last_history_by_item(item_obj["itemid"], history)[1]
                                    series_data = []
                                    for data in history_data:
                                        series_data.append(data.get("value"))
                                        clock = time.strftime('%Y-%m-%d  %H:%M',time.localtime(int(data.get("clock"))))
                                        if clock not in x_axis:
                                            x_axis.append(clock)
                                    series_data.reverse()
                                    series.append({
                                        "name": item_name,
                                        "type": "line",
                                        "data": series_data,
                                    })
                                else:

                                    history_data = zabbix_obj.get_last_history_by_item(item_obj["itemid"], history)[1]
                                    if history_data:
                                        if item_type != "2":
                                            series.append({
                                                "name":item_name,
                                                "value":history_data[0]["value"]
                                            })
                                            _tmp_data.append(float(history_data[0]["value"]))
                                        else:
                                            # series.append({
                                            #     "name": item_name,
                                            #     "value": history_data[0]["value"]
                                            # })
                                            _max_data = float(history_data[0]["value"])
                                            _max_item = item_name

                            if graph.get("graphtype") == "2":
                                series.append({
                                    "name": _max_item,
                                    "value": _max_data - sum(_tmp_data)
                                })

                        x_axis.reverse()
                        graph_list.append({
                            "legend": legend,
                            "series": series,
                            "unit": unit,
                            "graph_type":graph.get("graphtype"),
                            "x_axis":x_axis,
                            "name":graph.get("name"),
                            "graphid":graph.get("graphid")
                        })
            self.response_data["data"] = graph_list

        else:
            self.response_data["status"] = False
            self.status_code = 404
