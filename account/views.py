from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def account_login(request):
    """
    登录视图
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('/')
        else:
            return render(request, 'login.html', {"error": '用户名密码错误'})
    else:
        return render(request, 'login.html')


def account_logout(request):
    """
    退出视图
    :param request:
    :return:
    """
    logout(request)
    return redirect('/login/')
