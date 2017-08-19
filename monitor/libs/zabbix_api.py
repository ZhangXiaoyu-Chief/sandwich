from urllib import request, parse, error
import json
import socket
import re
import time

socket.setdefaulttimeout(5)


class ZabbixApi(object):
    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password
        self.__rpc_version = "2.0"
        self.__header = {"Content-Type": "application/json"}
        res = self.__auth()
        if res[0]:
            self.__token = res[1]
        else:
            self.__token = None
            # print(self.__token)

    def __http_request(self, method, params, request_id=1, token=None):
        """
        发送API请求方法
        :param method: 被调用的API方法
        :param params: 将传递给API方法的参数
        :param request_id: 请求的任意标识符
        :return: 结果
        """
        # print(params)
        request_data = {
            "jsonrpc": self.__rpc_version,
            "method": method,
            "params": params,
            "id": request_id,
            "auth": token
        }
        msg = ""
        result = None
        req = request.Request(self.__url, json.dumps(request_data).encode("utf-8"))
        for k, v in self.__header.items():
            req.add_header(k, v)
        try:
            result = request.urlopen(req)
        except error.ContentTooShortError:
            msg = "content is too short"
        except error.URLError:
            msg = "url error"
        except error.HTTPError:
            msg = "http error"
        finally:
            if result:
                result = json.loads(result.read().decode())
                if "result" in result:
                    return True, result.get("result")
                else:
                    return False, result.get("error", {}).get("data")
            else:
                return False, msg

    def __auth(self):
        params = {
            "user": self.__username,
            "password": self.__password
        }
        request_id = 1
        method = "user.login"

        res = self.__http_request(method, params, request_id)
        # print(res)
        return res

    def get_hosts(self):
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectInterfaces": [
                "interfaceid",
                "ip",
                "type"
            ],
            "selectParentTemplates": [
                "templateid",
                "name"
            ]
        }
        request_id = 2
        method = "host.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_groups(self):
        params = {
            "output": "extend"
        }

        request_id = 3
        method = "hostgroup.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_templates(self):
        params = {
            "output": "extend"
        }
        request_id = 3
        method = "template.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def create_host_by_agent(self, ip, name, groups, templates):
        params = {
            "host": name,
            "interfaces": [
                {
                    "type": 1,
                    "main": 1,
                    "useip": 1,
                    "ip": ip,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": groups,
            "templates": templates,
        }
        request_id = 4
        method = "host.create"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def delete_hosts(self, hostids):
        params = hostids
        request_id = 5
        method = "host.delete"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_hosts_by_id(self, hostid):
        params = {
            "hostids": hostid,
            "output": "extend",
            "selectGroups": "extend",
            "selectInterfaces": [
                "interfaceid",
                "ip",
                "type"
            ],
            "selectParentTemplates": [
                "templateid",
                "name"
            ]
        }
        request_id = 6
        method = "host.get"
        res = self.__http_request(method, params, request_id, self.__token)
        # print(res)
        return res

    def get_hosts_by_name(self, name):
        params = {
            "output": "extend",
            "selectGroups": "extend",
            "selectInterfaces": [
                "interfaceid",
                "ip",
                "type"
            ],
            "selectParentTemplates": [
                "templateid",
                "name"
            ],
            "filter": {
                "host": name
            }
        }
        request_id = 7
        method = "host.get"
        res = self.__http_request(method, params, request_id, self.__token)
        # print(res)
        return res

    def get_graph_by_id(self, hostid):
        params = {
            "hostids": hostid,
            "sortfield": "name"
        }

        request_id = 8
        method = "graph.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_item_by_graph(self, graphid):
        params = {
            "output": "extend",
            "graphids": graphid
        }

        request_id = 9
        method = "graphitem.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_history_by_item(self, itemid, history=3, starttime=None, endtime=None):
        nowtime = time.time()
        starttime = starttime if starttime else nowtime - 60 * 60
        endtime = endtime if endtime else nowtime
        params = {
            "output": "extend",
            "history": history,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "time_from": int(starttime),
            "time_till": int(endtime)
        }
        request_id = 10
        method = "history.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_item_by_host(self, hostid):
        params = {
            "output": "extend",
            "hostids": hostid,

            "sortfield": "name"
        }
        request_id = 11
        method = "item.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_item_by_id(self, itemid):
        params = {
            "output": "extend",
            "itemids": itemid,
            "sortfield": "name",

        }
        request_id = 12
        method = "item.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res

    def get_last_history_by_item(self, itemid, history=3):
        params = {
            "output": "extend",
            "history": history,
            "itemids": itemid,
            "sortfield": "clock",
            "sortorder": "DESC",
            "limit": 1
        }
        request_id = 13
        method = "history.get"
        res = self.__http_request(method, params, request_id, self.__token)
        return res


if __name__ == "__main__":
    url = "http://192.168.95.136/zabbix/api_jsonrpc.php"
    username = "Admin"
    password = "zabbix"
    zabbix_obj = ZabbixApi(url=url, username=username, password=password)
    host_info = zabbix_obj.get_hosts_by_name("zabbix-1")
    host_info = host_info[1] if host_info[0] else {}
    if host_info and host_info[0]:
        # print(host_info)
        host_id = host_info[0].get("hostid")
        # print(host_id)
        graphs = zabbix_obj.get_graph_by_id(host_id)
        # print(graphs)
        graph_list = []
        if graphs[0] and graphs[1]:
            for graph in graphs[1]:

                items = zabbix_obj.get_item_by_graph(graph.get("graphid"))
                print("_______________")
                print(graph.get("name"))
                # print(graph)series
                legend = []
                series = []
                unit = ""

                if items[0] and items[1]:
                    for item in items[1]:

                        item_type = item.get("type")
                        item_obj = zabbix_obj.get_item_by_id(item["itemid"])[1][0]
                        unit = item_obj.get("unit") if item_obj.get("unit") else ""
                        history = item_obj["value_type"]
                        item_name = item_obj.get("name")
                        keys = re.search(r"\[([^\]]*)\]", item_obj.get("key_"))
                        keys = keys.groups()[0] if keys else ""

                        for _key in keys.split(","):
                            item_name = item_name.replace("$%s" % (keys.index(_key) + 1), _key)

                        item_name = "%s 单位（%s）" % (item_name, item_obj.get("unit")) if item_obj.get("unit") else item_name
                        legend.append(item_name)
                        if item_type != 2:
                            history_data = zabbix_obj.get_history_by_item(item_obj["itemid"], history)[1]
                        else:
                            history_data = zabbix_obj.get_last_history_by_item(item_obj["itemid"], history)[1]
                        series_data = []
                        for data in history_data:
                            series_data.append(data.get("value"))
                        series.append({
                            "name": item_name,
                            "tpye": "line",
                            "data": series_data
                        })
                    # print(series)
                graph_list.append({
                    "legend":legend,
                    "series":series,
                    "unit":unit
                })
                # print(legend)
                # print(series)
            print(json.dumps(graph_list, indent=2))


    # print(json.dumps(zabbix_obj.get_hosts()[1], indent=2))
    # print(json.dumps(zabbix_obj.get_groups()[1], indent=2))
    # print(json.dumps(zabbix_obj.get_templates()[1], indent=2))
    # print(json.dumps(zabbix_obj.create_host_by_agent("192.168.95.134", "zabbix-3", [{"groupid":"2"}],[{"templateid":"10001"},])[1], indent=2))
    # print(json.dumps(zabbix_obj.delete_hosts(["10107"])[1], indent=2))
    # print(json.dumps(zabbix_obj.get_hosts_by_id(["10105","10084"])[1], indent=2))
    # print(json.dumps(zabbix_obj.get_hosts_by_name(["zabbix-1","Zabbix server"])[1], indent=2))
    # graphs = zabbix_obj.get_graph_by_id("10105")[1]
    # items = zabbix_obj.get_item_by_host("10105")[1]
    # # print(json.dumps(items, indent=2))
    # items = zabbix_obj.get_item_by_id(25400)[1]
    # # print(json.dumps(items, indent=2))
    # # exit()
    # for graph in graphs:
    #     # print(graph["name"])
    #     items = zabbix_obj.get_item_by_graph(graph["graphid"])
    #     print(items[1])
    #     for item_obj in items[1]:
    #         item_obj = zabbix_obj.get_item_by_id(item_obj["itemid"])[1][0]
    #         history = item_obj["value_type"]
    #         item_name = item_obj.get("name")
    #
    #         print(item_obj)
    #         # print(item_name)
    #         # print(item_obj.get("key_"))
    #         keys = re.search(r"\[([^\]]*)\]", item_obj.get("key_"))
    #
    #         keys = keys.groups()[0] if keys else ""
    #         # print(keys.split(","))
    #         for _key in keys.split(","):
    #             item_name = item_name.replace("$%s" % (keys.index(_key) + 1), _key)
    #         print(item_name)
    #         print(item_obj.get("units"))
    #         # print(item_obj.get("name"),1, item_obj.get("key_"),item_obj["itemid"])
    #         # print(history[1][0]["value_type"])
    #         history_data = zabbix_obj.get_history_by_item(item_obj["itemid"], history)[1]
    #         # print(item_obj)
    #         print(time.time())
    #         print(history_data)
    #         #     break
    #         # break
    #
    #
    #         # print(json.dumps(zabbix_obj.get_graph_by_id("10105")[1], indent=2))
    #         # print(json.dumps(zabbix_obj.get_item_by_graph(549)[1], indent=2))
    #         # print(json.dumps(zabbix_obj.get_history_by_item("23258")[1], indent=2))
