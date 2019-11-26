# Generated by Django 2.2.7 on 2019-11-24 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('operation', '0001_initial'),
        ('examination', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='wrongquestion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='usermessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='sectionrecord',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Question', verbose_name='做到哪一题'),
        ),
        migrations.AddField(
            model_name='sectionrecord',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Section', verbose_name='所属节'),
        ),
        migrations.AddField(
            model_name='sectionrecord',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='questionfeedback',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Question', verbose_name='反馈问题'),
        ),
        migrations.AddField(
            model_name='questionfeedback',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='反馈用户'),
        ),
        migrations.AddField(
            model_name='questionfav',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Question', verbose_name='收藏问题'),
        ),
        migrations.AddField(
            model_name='questionfav',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='examscore',
            name='examination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Examination', verbose_name='所属试卷'),
        ),
        migrations.AddField(
            model_name='examscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='dayscore',
            name='day_attendance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.DayAttendance', verbose_name='所属日期'),
        ),
        migrations.AddField(
            model_name='dayscore',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='examination.Question', verbose_name='做到哪一题'),
        ),
        migrations.AddField(
            model_name='dayscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]