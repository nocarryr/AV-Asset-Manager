# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-20 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_category_linked_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='linked_categories',
            field=models.ManyToManyField(blank=True, to='categories.Category'),
        ),
    ]
