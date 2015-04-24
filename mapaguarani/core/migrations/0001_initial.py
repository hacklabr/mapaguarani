# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('file', models.FileField(verbose_name='attached file', upload_to='')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentationType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='GuaraniPresence',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('presence', models.BooleanField(verbose_name='Guarani presence')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(max_length=512, verbose_name='name')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='LandsLayer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('other_names', models.CharField(max_length=512, verbose_name='name')),
                ('official_area', models.FloatField(verbose_name='')),
                ('guarani_exclusive_possession_area_portion', models.FloatField(null=True, verbose_name='Guarani full and exclusive portion area possession', blank=True)),
                ('others_exclusive_possession_area_portion', models.FloatField(null=True, verbose_name='Others people full and exclusive portion area possession', blank=True)),
                ('claim', models.TextField(null=True, verbose_name='Clain', blank=True)),
                ('demand', models.TextField(null=True, verbose_name='Demand', blank=True)),
                ('source', models.CharField(max_length=512, verbose_name='name')),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(related_name='landslayer_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='ethnic group')),
                ('prominent_subgroup', models.ManyToManyField(related_name='landslayer_prominent_subgroup_layers', to='core.EthnicGroup', verbose_name='prominent ethnic sub-group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegalProceedings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='Description')),
                ('indigenous_land_layer', models.ForeignKey(to='core.LandsLayer', verbose_name='Guarani indigenous lands layer')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('population', models.IntegerField(verbose_name='Population')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(max_length=512, verbose_name='name')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='VillagesLayer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('other_names', models.CharField(max_length=512, verbose_name='name')),
                ('comments', models.TextField(null=True, verbose_name='Comments', blank=True)),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(related_name='villageslayer_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='ethnic group')),
                ('prominent_subgroup', models.ManyToManyField(related_name='villageslayer_prominent_subgroup_layers', to='core.EthnicGroup', verbose_name='prominent ethnic sub-group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='population',
            name='village',
            field=models.ForeignKey(verbose_name='Village', related_name='population_annual_series_population', to='core.VillagesLayer'),
        ),
        migrations.AddField(
            model_name='legalproceedings',
            name='indigenous_village_layer',
            field=models.ForeignKey(to='core.VillagesLayer', verbose_name='Guarani indigenous villages layer'),
        ),
        migrations.AddField(
            model_name='guaranipresence',
            name='village',
            field=models.ForeignKey(to='core.VillagesLayer', verbose_name='Village'),
        ),
        migrations.AddField(
            model_name='documentation',
            name='type',
            field=models.ForeignKey(to='core.DocumentationType', verbose_name='type'),
        ),
    ]
