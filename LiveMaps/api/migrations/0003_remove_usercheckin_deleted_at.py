# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-01 04:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180331_2235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercheckin',
            name='deleted_at',
        ),
    ]
