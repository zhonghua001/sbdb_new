# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-07 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bkrs', '0007_backuphostconf_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backuphostconf',
            name='xtrabackup_conf',
            field=models.CharField(max_length=8000, null=True),
        ),
    ]