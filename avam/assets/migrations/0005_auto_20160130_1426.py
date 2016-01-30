# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-30 20:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20160130_1419'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='temp_date_acquired',
            new_name='date_acquired',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='temp_notes',
            new_name='notes',
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='temp_retired',
            new_name='retired',
        ),
        migrations.RemoveField(
            model_name='genericaccessory',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='genericaccessory',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='genericaccessory',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='genericaccessory',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='genericasset',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='genericasset',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='genericasset',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='genericasset',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='ledlight',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='ledlight',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='ledlight',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='ledlight',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='movinglight',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='movinglight',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='movinglight',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='movinglight',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='movinglightlamp',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='movinglightlamp',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='movinglightlamp',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='movinglightlamp',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='projector',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='projector',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='projector',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='projector',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='projectorfilter',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='projectorfilter',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='projectorfilter',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='projectorfilter',
            name='retired',
        ),
        migrations.RemoveField(
            model_name='projectorlamp',
            name='date_acquired',
        ),
        migrations.RemoveField(
            model_name='projectorlamp',
            name='in_use',
        ),
        migrations.RemoveField(
            model_name='projectorlamp',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='projectorlamp',
            name='retired',
        ),
    ]