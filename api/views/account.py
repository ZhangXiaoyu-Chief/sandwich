from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
from account.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


class Account(CoreView):
    """
    用户相关接口
    """
    def get_list(self):
        """
        获取用户列表接口
        :return: 
        """
        user_list = []
        user_objs = UserProfile.objects.all()
        for user_obj in user_objs:
            user_list.append(user_obj.get_info())
        self.response_data['data'] = user_list

    def post_create(self):
        """
        创建用户接口
        :return: 
        """
        username = self.parameters('username')
        password = self.parameters('password')
        email = self.parameters('email')
        is_active = True if self.parameters('active') == 'true' else False
        is_superuser = True if self.parameters('is_superuser') == 'true' else False
        nickname = self.parameters('nickname')
        avatar = self.parameters('avatar')
        user_obj = User.objects.create(username=username, password=password, email=email,
                                       is_superuser=is_superuser, is_active=is_active)
        user_profile_obj = UserProfile.objects.create(user=user_obj, nickname=nickname, avatar=avatar)

        self.response_data['data'] = user_profile_obj.get_info()
