# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150727_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indigenousland',
            name='official_area',
            field=models.FloatField(null=True, blank=True, verbose_name='Official area'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='other_names',
            field=models.CharField(null=True, blank=True, max_length=512, verbose_name='Others names'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='Indigenous Land Spatial Data'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='other_names',
            field=models.CharField(null=True, blank=True, max_length=512, verbose_name='Others names'),
        ),
    ]
