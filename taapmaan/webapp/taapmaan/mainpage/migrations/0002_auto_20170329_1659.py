# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-29 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensordata',
            name='sensor',
        ),
        migrations.DeleteModel(
            name='SensorData',
        ),
    ]