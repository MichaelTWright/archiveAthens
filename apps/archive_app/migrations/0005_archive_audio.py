# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-26 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive_app', '0004_auto_20181025_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='archive',
            name='audio',
            field=models.FileField(default='none', upload_to='audio'),
            preserve_default=False,
        ),
    ]
