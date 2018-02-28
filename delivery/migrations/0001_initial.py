# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-26 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appconf', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='\u9879\u76ee\u63cf\u8ff0')),
                ('deploy_policy', models.CharField(choices=[('Direct', 'Direct')], max_length=255, verbose_name='\u90e8\u7f72\u7b56\u7565')),
                ('version', models.CharField(blank=True, max_length=255, verbose_name='\u7248\u672c\u4fe1\u606f')),
                ('build_clean', models.BooleanField(default=False, verbose_name='\u6e05\u7406\u6784\u5efa')),
                ('shell', models.CharField(blank=True, max_length=255, verbose_name='shell')),
                ('shell_position', models.BooleanField(default=False, verbose_name='\u672c\u5730\u6267\u884c')),
                ('status', models.BooleanField(default=False, verbose_name='\u90e8\u7f72\u72b6\u6001')),
                ('deploy_num', models.IntegerField(default=0, verbose_name='\u90e8\u7f72\u6b21\u6570')),
                ('bar_data', models.IntegerField(default=0)),
                ('auth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appconf.AuthInfo', verbose_name='\u8ba4\u8bc1\u4fe1\u606f')),
                ('job_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appconf.Project', verbose_name='\u9879\u76ee\u540d')),
            ],
        ),
    ]