# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-27 07:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190727_1459'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='create_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='create_time',
            new_name='created_time',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='ower',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='stauts',
            new_name='status',
        ),
    ]
