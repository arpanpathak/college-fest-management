# Generated by Django 2.0.1 on 2018-02-09 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0018_auto_20180209_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='teamName',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
