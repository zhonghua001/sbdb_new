# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-28 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_mysql_monitor_table_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='Binlog_datetime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binlog_file', models.CharField(max_length=50)),
                ('binlog_pos', models.CharField(max_length=30)),
                ('start_date', models.CharField(max_length=25)),
                ('end_date', models.CharField(max_length=25)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Db_instance')),
            ],
        ),
    ]