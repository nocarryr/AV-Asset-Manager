# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20160131_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='serial_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
