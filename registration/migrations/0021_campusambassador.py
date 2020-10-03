# Generated by Django 2.0.2 on 2018-02-20 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('default', '0002_auto_20180209_0003'),
        ('registration', '0020_auto_20180209_2313'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampusAmbassador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('contactNo', models.CharField(max_length=10)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='default.College')),
            ],
        ),
    ]
