from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=u'用户名', on_delete=models.CASCADE, related_name="userprofile")
    nickname = models.CharField(max_length=32, verbose_name=u'昵称')
    avatar = models.CharField(max_length=300, blank=True, null=True, verbose_name=u'头像')

    def __str__(self):
        return self.nickname

    def __unicode__(self):
        return self.nickname

    def get_info(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "nickname": self.nickname if self.nickname else "",
            "avatar": self.avatar if self.avatar else "",
            "email": self.user.email,
            "is_superuser": self.user.is_superuser,
            "status": self.user.is_active,
            "create_date": self.user.date_joined.strftime("%Y-%m-%d %H:%M"),
            # "last_date": self.user.get_latest_by()
            "group": [{"id": group.id, "name": group.name} for group in self.user.groups.all()]
        }

    class Meta:
        verbose_name = u'用户资料'
        verbose_name_plural = u'用户资料'



