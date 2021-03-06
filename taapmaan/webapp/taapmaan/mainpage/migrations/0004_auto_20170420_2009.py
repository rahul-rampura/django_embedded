# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_sensordata'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sensordata',
            options={'ordering': ('-time',)},
        ),
        migrations.AddField(
            model_name='sensor',
            name='retrospect_period',
            field=models.IntegerField(default='15'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='threshold',
            field=models.IntegerField(default=35),
        ),
        migrations.AddField(
            model_name='sensor',
            name='time_period',
            field=models.IntegerField(default=5),
        ),
    ]
