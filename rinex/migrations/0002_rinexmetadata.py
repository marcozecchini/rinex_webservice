# Generated by Django 3.0.7 on 2020-07-16 13:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rinex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RinexMetadata',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_lon', models.FloatField()),
                ('min_lat', models.FloatField()),
                ('max_lon', models.FloatField()),
                ('max_lat', models.FloatField()),
                ('receiver_info', models.CharField(max_length=100)),
                ('antenna_info', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('system_info', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), size=None)),
                ('number_sys_info', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('dual_frequency', django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), size=None)),
                ('file_rinex', models.BinaryField()),
                ('upload_datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
