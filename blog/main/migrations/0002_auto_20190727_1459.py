# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-27 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='create_time',
            new_name='created_time',
        ),
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(auto_created=True, editable=False, verbose_name='创建时间'),
        ),
    ]
