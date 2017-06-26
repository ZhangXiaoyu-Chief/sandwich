from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
from account.models import UserProfile
from django.contrib.auth.models import User
# Create your views here.


class Account(CoreView):
    """
    用户相关接口
    """
    login_required_action = ["get_list", "post_create", "post_forbidden", "get_user"]
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

    def post_disable(self):
        user_id = self.parameters("user_id")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj and user_profile_obj.user:
            user_profile_obj.user.is_active = False
            user_profile_obj.user.save()
        else:
            self.response_data['data'] = "要编辑的用户不存在"
            self.status_code = 404
        self.response_data['data'] = user_profile_obj.get_info()

    def post_enable(self):
        user_id = self.parameters("user_id")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj and user_profile_obj.user:
            user_profile_obj.user.is_active = True
            user_profile_obj.user.save()
        else:
            self.response_data['data'] = "要编辑的用户不存在"
            self.status_code = 404
        self.response_data['data'] = user_profile_obj.get_info()

    def get_user(self):
        user_id = self.parameters("user_id")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj:
            self.response_data['data'] = user_profile_obj.get_info()
        else:
            self.response_data['info'] = "要编辑的用户不存在"
            self.status_code = 404
