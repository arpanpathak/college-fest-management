# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 21:21
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_candidate_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 23, 2, 51, 8, 32229), editable=False),
        ),
    ]
