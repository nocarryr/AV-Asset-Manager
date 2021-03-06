# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-03 18:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('assettypes', '0004_auto_20160203_1243'),
        ('assets', '0011_videocamera'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectorLens',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Asset')),
                ('asset_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='assettypes.ProjectorLensModel')),
                ('installed_in', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lens', to='assets.Projector')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=('assets.asset', models.Model),
        ),
        migrations.CreateModel(
            name='VideoCameraLens',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='assets.Asset')),
                ('asset_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='assettypes.CameraLensModel')),
                ('installed_in', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lens', to='assets.VideoCamera')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.Location')),
            ],
            options={
                'abstract': False,
            },
            bases=('assets.asset', models.Model),
        ),
    ]
