# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-04 19:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventman', '0003_event_maxisbetter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='maxIsBetter',
        ),
    ]