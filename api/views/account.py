from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
from account.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.utils import IntegrityError
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
        try:
            username = self.parameters('username')
            password = self.parameters('password')
            email = self.parameters('email')
            group_ids = self.parameters("group").split(",")
            group_objs = Group.objects.filter(id__in=group_ids).all()
            is_active = True if self.parameters('status') == 'true' else False
            is_superuser = True if self.parameters('is_superuser') == 'true' else False
            nickname = self.parameters('nickname')
            avatar = self.parameters('avatar')
            user_obj = User.objects.create(username=username, password=password, email=email,
                                           is_superuser=is_superuser, is_active=is_active)
            for group_obj in group_objs:
                user_obj.groups.add(group_obj)
            user_obj.save()
            user_profile_obj = UserProfile.objects.create(user=user_obj, nickname=nickname, avatar=avatar)

            self.response_data['data'] = user_profile_obj.get_info()
        except IntegrityError:
            self.response_data['status'] = False
            self.status_code = 416


    # def post_disable(self):
    #     user_id = self.parameters("user_id")
    #     user_profile_obj = UserProfile.objects.filter(id=user_id).first()
    #     if user_profile_obj and user_profile_obj.user:
    #         user_profile_obj.user.is_active = False
    #         user_profile_obj.user.save()
    #     else:
    #         self.response_data['status'] = False
    #         self.response_data['data'] = "要编辑的用户不存在"
    #         self.status_code = 404
    #     self.response_data['data'] = user_profile_obj.get_info()
    #
    # def post_enable(self):
    #     user_id = self.parameters("user_id")
    #     user_profile_obj = UserProfile.objects.filter(id=user_id).first()
    #     if user_profile_obj and user_profile_obj.user:
    #         user_profile_obj.user.is_active = True
    #         user_profile_obj.user.save()
    #     else:
    #         self.response_data['status'] = False
    #         self.response_data['data'] = "要编辑的用户不存在"
    #         self.status_code = 404
    #     self.response_data['data'] = user_profile_obj.get_info()

    def post_change_status(self):
        user_id = self.parameters("user_id")
        is_active = True if self.parameters('status') == 'true' else False
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj and user_profile_obj.user:
            user_profile_obj.user.is_active = is_active
            user_profile_obj.user.save()
        else:
            self.response_data['status'] = False
            self.response_data['data'] = "要编辑的用户不存在"
            self.status_code = 404
        self.response_data['data'] = user_profile_obj.get_info()

    def get_user(self):
        user_id = self.parameters("user_id")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj:
            self.response_data['data'] = user_profile_obj.get_info()
        else:
            self.status_code = 404

    def post_change(self):
        """
        编辑用户接口
        :return: 
        """
        user_id = self.parameters('id')
        username = self.parameters('username')
        email = self.parameters('email')
        is_active = True if self.parameters('status') == 'true' else False
        is_superuser = True if self.parameters('is_superuser') == 'true' else False
        nickname = self.parameters('nickname')
        avatar = self.parameters('avatar')
        group_ids = self.parameters("group").split(",")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()

        group_objs = Group.objects.filter(id__in=group_ids).all()

        if user_profile_obj:
            try:
                user_profile_obj.user.username = username
                user_profile_obj.user.email = email
                user_profile_obj.user.is_active = is_active
                user_profile_obj.user.is_superuser = is_superuser
                user_profile_obj.user.groups = []
                for group_obj in group_objs:
                    user_profile_obj.user.groups.add(group_obj)
                user_profile_obj.user.save()
                user_profile_obj.avatar = avatar
                user_profile_obj.nickname = nickname
                user_profile_obj.save()
            except IntegrityError:
                self.response_data['status'] = False
                self.status_code = 416
        else:
            self.response_data['status'] = False
            self.status_code = 404

    def post_changepwd(self):
        """
        修改密码视图
        """
        newpassword = self.parameters("newpassword")
        user_id = self.parameters("user_id")
        user_profile_obj = UserProfile.objects.filter(id=user_id).first()
        if user_profile_obj:
            user_profile_obj.user.set_password(newpassword)
            user_profile_obj.user.save()
        else:
            self.response_data['status'] = False
            self.status_code = 404
