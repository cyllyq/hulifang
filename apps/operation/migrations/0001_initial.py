# Generated by Django 2.2.7 on 2019-11-24 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('examination', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('score', models.PositiveIntegerField(verbose_name='成绩')),
                ('is_done', models.BooleanField(default=False, verbose_name='是否做完')),
            ],
            options={
                'verbose_name': '每日打卡成绩',
                'verbose_name_plural': '每日打卡成绩',
            },
        ),
        migrations.CreateModel(
            name='ExamScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('score', models.PositiveIntegerField(verbose_name='成绩')),
            ],
            options={
                'verbose_name': '试卷成绩',
                'verbose_name_plural': '试卷成绩',
            },
        ),
        migrations.CreateModel(
            name='QuestionFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '问题收藏',
                'verbose_name_plural': '问题收藏',
            },
        ),
        migrations.CreateModel(
            name='QuestionFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('comment', models.CharField(db_index=True, max_length=500, verbose_name='反馈内容')),
                ('has_handle', models.BooleanField(default=False, verbose_name='是否处理')),
            ],
            options={
                'verbose_name': '问题反馈',
                'verbose_name_plural': '问题反馈',
            },
        ),
        migrations.CreateModel(
            name='SectionRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_done', models.BooleanField(default=False, verbose_name='是否做完')),
            ],
            options={
                'verbose_name': '做到哪一题',
                'verbose_name_plural': '做到哪一题',
            },
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('message', models.CharField(max_length=300, verbose_name='信息')),
                ('has_read', models.BooleanField(default=False, verbose_name='是否已读')),
            ],
            options={
                'verbose_name': '系统消息',
                'verbose_name_plural': '系统消息',
            },
        ),
        migrations.CreateModel(
            name='WrongQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.Question', verbose_name='错题')),
            ],
            options={
                'verbose_name': '错题集',
                'verbose_name_plural': '错题集',
            },
        ),
    ]
