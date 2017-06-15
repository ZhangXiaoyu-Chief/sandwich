from django.shortcuts import render, HttpResponse
from cmdb.models import Asset, Server, CPU, RAM, Disk, NIC ,Manufactory


# Create your views here.


def index(request):
    serverinfo = {
        "cpu_information": {
            "manufactory": "GenuineIntel",
            "cpu_count": 1,
            "cpu_core_count": 1,
            "cpu_model": "Intel(R) Xeon(R) CPU E5-2682 v4 @ 2.50GHz"
        },
        "essential_information": {
            "manufactory": "Alibaba Cloud",
            "os_type": "Ubuntu",
            "kernel_release": "4.4.0-63-generic",
            "SN": "5ad48cfe-3cbf-4110-ac46-95d697e213bf",
            "os_release": "14.04",
            "os_distribution": "Ubuntu 14.04.5 LTS",
            "model": "Alibaba Cloud ECS",
            "hostname": "iZ2ze4cwodiz4t64z887v4Z"
        },
        "disk_information": [
            {
                "capacity": 40960,
                "name": "vda"
            },
            {
                "capacity": 20480,
                "name": "vdb"
            },
            {
                "capacity": 1024,
                "name": "sr0"
            }
        ],
        "interfaces_information": [
            {
                "ip_address": "127.0.0.1",
                "netmask": "255.0.0.0",
                "name": "lo",
                "macaddress": ""
            },
            {
                "ip_address": "172.17.199.190",
                "netmask": "255.255.240.0",
                "name": "eth0",
                "macaddress": "00:16:3e:06:3e:76"
            }
        ],
        "memory_information": {
            "capacity": 992
        }
    }
    # factory_obj = Manufactory()
    # factory_obj.save()


    # print(factory_obj)
    # factory_obj.save()
    # asset_obj = Asset(asset_type='server',
    #                   name=serverinfo['essential_information']['hostname'],
    #                   sn=serverinfo['essential_information']['SN'],
    #                   manufactory=factory_obj,
    #                   status=0
    #                   )
    # asset_obj.save()
    # server_obj = Server(asset=asset_obj,
    #                     created_by='auto',
    #                     model=serverinfo['essential_information']['model'],
    #                     os_type=serverinfo['essential_information']['os_type'],
    #                     os_distribution=serverinfo['essential_information']['os_distribution'],
    #                     os_release=serverinfo['essential_information']['os_release'],
    #                     kernel_release=serverinfo['essential_information']['kernel_release'],
    #                     )
    # server_obj.save()

    # factory_obj = Manufactory.objects.filter(name=serverinfo['cpu_information']['manufactory'], ).first()
    # if not factory_obj:
    #     factory_obj = Manufactory(name=serverinfo['cpu_information']['manufactory'])
    #     factory_obj.save()
    # asset_obj = Asset.objects.filter(name=serverinfo['essential_information']['hostname']).first()
    # print(asset_obj)
    # cpu_obj = CPU(asset=asset_obj,
    #               model=serverinfo['cpu_information']['cpu_model'],
    #               count=serverinfo['cpu_information']['cpu_count'],
    #               core_count=serverinfo['cpu_information']['cpu_core_count'],
    #               )
    # cpu_obj.save()

    # asset_obj = Asset.objects.filter(name=serverinfo['essential_information']['hostname']).first()
    # print(asset_obj)
    # for diskinfo in serverinfo['disk_information']:
    #     disk_obj = Disk(name=diskinfo['name'],
    #                     capacity=diskinfo['capacity'],
    #                     asset=asset_obj
    #                     )
    #     disk_obj.save()


    # asset_obj = Asset.objects.filter(name=serverinfo['essential_information']['hostname']).first()
    # print(asset_obj)
    #
    # for nic_info in serverinfo['interfaces_information']:
    #     nic_obj = NIC(asset=asset_obj,
    #                   name=nic_info['name'],
    #                   ip_address=nic_info['ip_address'],
    #                   netmask=nic_info['netmask'],
    #                   mac_address=nic_info['macaddress']
    #                   )
    #     nic_obj.save()


    # asset_obj = Asset.objects.filter(name=serverinfo['essential_information']['hostname']).first()
    # print(asset_obj)
    #
    # ram_obj = RAM(asset=asset_obj,capacity=serverinfo['memory_information']['capacity'])
    # ram_obj.save()
    return render(request, 'index.html', {})


def get_server_list(request):
    import json
    server_objs = Asset.objects.filter(asset_type='server').all()
    server_list = []
    for server_obj in server_objs:
        server_list.append(server_obj.get_base_info())
    return HttpResponse(json.dumps(server_list))
