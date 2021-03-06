# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 01:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilterModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('filter_type', models.CharField(choices=[('w', 'Washable'), ('c', 'Cartridge'), ('s', 'Scrolling')], max_length=1)),
                ('max_hours', models.PositiveIntegerField(blank=True, null=True)),
                ('replaceable', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericAccessoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GenericModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LampModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('max_hours', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LEDLightModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MovingLightModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('lamp_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.LampModel')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer')),
                ('other_accessories', models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectorModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('lamp_count', models.PositiveIntegerField(default=1)),
                ('filter_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assettypes.FilterModel')),
                ('lamp_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.LampModel')),
                ('manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer')),
                ('other_accessories', models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ledlightmodel',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer'),
        ),
        migrations.AddField(
            model_name='ledlightmodel',
            name='other_accessories',
            field=models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel'),
        ),
        migrations.AddField(
            model_name='lampmodel',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer'),
        ),
        migrations.AddField(
            model_name='lampmodel',
            name='other_accessories',
            field=models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel'),
        ),
        migrations.AddField(
            model_name='genericmodel',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer'),
        ),
        migrations.AddField(
            model_name='genericmodel',
            name='other_accessories',
            field=models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel'),
        ),
        migrations.AddField(
            model_name='genericaccessorymodel',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer'),
        ),
        migrations.AddField(
            model_name='genericaccessorymodel',
            name='other_accessories',
            field=models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel'),
        ),
        migrations.AddField(
            model_name='filtermodel',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assettypes.Manufacturer'),
        ),
        migrations.AddField(
            model_name='filtermodel',
            name='other_accessories',
            field=models.ManyToManyField(blank=True, to='assettypes.GenericAccessoryModel'),
        ),
        migrations.AlterUniqueTogether(
            name='projectormodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='genericmodel',
            unique_together=set([('manufacturer', 'model_name')]),
        ),
    ]
