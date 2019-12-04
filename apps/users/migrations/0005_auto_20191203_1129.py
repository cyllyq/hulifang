# Generated by Django 2.2.7 on 2019-12-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20191202_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifycode',
            name='user',
        ),
        migrations.AddField(
            model_name='verifycode',
            name='is_used',
            field=models.BooleanField(default=False, verbose_name='是否使用'),
        ),
        migrations.AddField(
            model_name='verifycode',
            name='mobile',
            field=models.CharField(db_index=True, default=18337123711, max_length=11, verbose_name='用户'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='expire_time',
            field=models.DateTimeField(db_index=True, verbose_name='过期时间'),
        ),
    ]
