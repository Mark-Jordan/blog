# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-28 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20190727_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(auto_created=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='main.Tag', verbose_name='标签'),
        ),
    ]
