# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0013_eventresult_scoresubmittedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventresult',
            name='timeStamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
