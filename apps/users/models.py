from apps.abstract import TimeModel

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


_User = settings.AUTH_USER_MODEL

class User(AbstractUser, TimeModel):
    #username = models.CharField(max_length=50, db_index=True, verbose_name=u'昵称')
    coin = models.PositiveIntegerField(default=0, verbose_name=u'金币')
    mobile = models.CharField(max_length=11, db_index=True, unique=True, verbose_name='手机')
    image = models.CharField(default=0, max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(TimeModel):
    mobile = models.CharField(max_length=11, db_index=True, verbose_name=u'用户')
    code = models.CharField(max_length=11, verbose_name='验证码',)
    expire_time = models.DateTimeField(db_index=True, verbose_name=u'过期时间',)
    is_used = models.BooleanField(default=False, verbose_name='是否使用')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '短信验证码'+self.code