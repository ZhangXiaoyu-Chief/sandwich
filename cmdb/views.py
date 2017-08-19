from django.shortcuts import render, HttpResponse
from cmdb.models import Asset, Server, CPU, RAM, Disk, NIC ,Manufactory
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html', {})


# def get_server_list(request):
#     import json
#     server_objs = Asset.objects.filter(asset_type='server').all()
#     server_list = []
#     for server_obj in server_objs:
#         server_list.append(server_obj.get_base_info())
#     return HttpResponse(json.dumps(server_list))

def login(request):
    return render(request, 'login.html', {})
