from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'用户名', on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32, verbose_name=u'昵称')
    avatar = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'头像')

    class Meta:
        verbose_name = u'用户资料'
        verbose_name_plural = u'用户资料'
