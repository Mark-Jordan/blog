# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-30 00:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='link',
            old_name='herf',
            new_name='href',
        ),
    ]
