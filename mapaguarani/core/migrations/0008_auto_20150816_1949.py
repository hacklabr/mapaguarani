# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150816_1947'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandTenure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('map_color', models.CharField(verbose_name='Color in Map', max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Land Tenures',
                'verbose_name': 'Land Tenure',
            },
        ),
        migrations.CreateModel(
            name='LandTenureStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='Name', max_length=255)),
                ('map_color', models.CharField(verbose_name='Color in Map', max_length=64)),
            ],
            options={
                'verbose_name_plural': 'Land Tenures',
                'verbose_name': 'Land Tenure',
            },
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='land_tenure',
            field=models.ForeignKey(to='core.LandTenure', related_name='indigenous_lands', blank=True, null=True, verbose_name='Land Tenure'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='land_tenure_status',
            field=models.ForeignKey(to='core.LandTenureStatus', related_name='indigenous_lands', blank=True, null=True, verbose_name='Land Tenure Status'),
        ),
    ]
