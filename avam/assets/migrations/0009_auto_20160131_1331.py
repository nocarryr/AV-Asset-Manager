# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-31 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0008_auto_20160131_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
