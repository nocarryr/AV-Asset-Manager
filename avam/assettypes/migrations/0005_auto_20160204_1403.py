# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 20:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assettypes', '0004_auto_20160203_1243'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cameralensmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='genericaccessorymodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='ledlightmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='movinglightlampmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='movinglightmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectorfiltermodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectorlampmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectorlensmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
    ]
