from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    #username = models.CharField(max_length=50, db_index=True, verbose_name=u'昵称')
    coin = models.PositiveIntegerField(default=0, verbose_name=u'金币')
    mobile = models.CharField(max_length=11, db_index=True, verbose_name='手机')
    image = models.CharField(default=0, max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
