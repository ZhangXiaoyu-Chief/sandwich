#!/usr/bin/env python
# -*- coding=utf-8 -*-
from .ansible_client import ANSRunner
import json


class CmdbCollector(object):
    def __init__(self, host, username, password, ssh_port=22):
        self.host = host
        self.username = username
        self.password = password
        self.ssh_port = ssh_port
        self.data = {}
        self.status = False
        self.msg = ""

        self.resource = [{"hostname": self.host,
                          "port": self.ssh_port,
                          "username": self.username,
                          "password": self.password}]
        self.asset_info = {
            "essential_information": {
                "SN": "",
                "hostname": "",
                "model": "",
                "manufactory": "",
                "kernel_release": "",
                "os_type": "",
                "os_distribution": "",
                "os_release": ""

            },
            "cpu_information": {
                "cpu_model": "",
                "cpu_count": 0,
                "cpu_core_count": 0,
                "manufactory": ""
            },
            "memory_information": {
                "capacity": 0
            },
            "interfaces_information": [],
            "disk_information": []

        }
        self.res = None

    def __collector_cpu_info(self):
        if self.res:
            cpu_info = self.asset_info.get("cpu_information")
            cpu_info["cpu_model"] = self.res.get("ansible_processor")[1] if self.res.get("ansible_processor") else ""
            cpu_info["manufactory"] = self.res.get("ansible_processor")[0] if self.res.get("ansible_processor") else ""
            cpu_info["cpu_count"] = self.res.get("ansible_processor_count")
            cpu_info["cpu_core_count"] = self.res.get("ansible_processor_cores", 0)

    def __collector_essential_info(self):
        if self.res:
            essential_info = self.asset_info.get("essential_information")
            essential_info["SN"] = self.res.get("ansible_product_serial") \
                if not self.res.get("ansible_product_serial") == "NA" else self.res.get("ansible_hostname")
            essential_info["os_release"] = self.res.get("ansible_lsb", {}).get("release")
            essential_info["kernel_release"] = self.res.get("ansible_kernel", "")
            essential_info["model"] = self.res.get("ansible_product_name", "")
            essential_info["manufactory"] = self.res.get("ansible_system_vendor", "")
            essential_info["os_type"] = self.res.get("ansible_lsb", {}).get("id")
            essential_info["os_distribution"] = self.res.get("ansible_lsb", {}).get("description")
            essential_info["hostname"] = self.res.get("ansible_hostname")

    def __collector_mem_info(self):
        if self.res:
            memory_info = self.asset_info.get("memory_information")
            # print(self.res)
            memory_info["capacity"] = self.res.get("ansible_memtotal_mb", 0)

    def __collector_nic_info(self):
        if self.res:
            print(self.res)
            nic_info = self.asset_info.get("interfaces_information")
            for interface in self.res.get("ansible_interfaces"):
                temp_nic_info = self.res.get("ansible_%s" % interface).get("ipv4") \
                    if "ipv4" in self.res.get("ansible_%s" % interface) else \
                    self.res.get("ansible_%s" % interface).get("ipv4_secondaries", [{}])[0]
                if not (interface.replace("_", ":") == "lo" or temp_nic_info.get("address", "") == "127.0.0.1"):
                    nic_info.append({
                        "name": interface.replace("_", ":"),
                        "ip_address": temp_nic_info.get("address", ""),
                        "netmask": temp_nic_info.get("netmask", ""),
                        "macaddress": self.res.get("ansible_%s" % interface).get("macaddress", ""),
                    })

    def __collector_disk_info(self):
        unit_map = {
            "MB": 1.0,
            "GB": 1024.0,
            "TB": 1024.0 * 1024.0
        }
        if self.res:
            disk_information = self.asset_info.get("disk_information")
            for disk_name, disk_info in self.res.get("ansible_devices", []).items():
                disk_information.append({
                    "name": disk_name,
                    "capacity": unit_map.get(disk_info.get("size").split(" ")[1], 1.0) * float(
                        disk_info.get("size").split(" ")[0])
                })

    def collector_all(self):
        rbt = ANSRunner(self.resource)  # resource可以是列表或者字典形式，如果做了ssh-key认证，就不会通过账户密码方式认证
        rbt.run_model(host_list=["default_group"], module_name='setup', module_args="")
        self.data = rbt.get_model_result()
        if self.data.get("success"):
            self.res = self.data.get("success").get(self.host).get("ansible_facts")
            self.__collector_essential_info()
            self.__collector_cpu_info()
            self.__collector_mem_info()
            self.__collector_nic_info()
            self.__collector_disk_info()
            self.status = True
        else:
            self.msg = self.data.get('failed').get(self.host, {}).get('msg',"") if self.data.get('failed') else self.data.get('unreachable').get(self.host, {}).get('msg',"")
        print(self.msg)
        print(json.dumps(self.asset_info, indent=2))


if __name__ == '__main__':
    cmdb_collector = CmdbCollector(host="192.168.95.131", username="zhangxiaoyu", password="123.com")
    cmdb_collector.collector_all()
