# Generated by Django 2.2.7 on 2019-12-03 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20191124_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectionrecord',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.SectionQuestion', verbose_name='做到哪一题'),
        ),
    ]
