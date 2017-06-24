from django.shortcuts import render, HttpResponse
from api.libs.base import CoreView
from account.models import UserProfile
# Create your views here.


class Account(CoreView):
    """
    
    """
    def get_list(self):
        user_list = []
        user_objs = UserProfile.objects.all()
        for user_obj in user_objs:
            user_list.append(user_obj.get_info())
        self.response_data['data'] = user_list

    def post_create(self):

        print(self.request.POST)
