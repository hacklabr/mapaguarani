# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchaeologicalPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('acronym', models.CharField(verbose_name='name', max_length=512)),
                ('position_precision', models.CharField(verbose_name='Position Precision', max_length=128, choices=[('exact', 'Exact'), ('estimated', 'Estimated'), ('by_city', 'By City'), ('no_position', 'No position')])),
                ('position_comments', models.TextField(verbose_name='Position Comments')),
            ],
        ),
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file', models.FileField(upload_to='', verbose_name='attached file')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(null=True, blank=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentationType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GuaraniPresence',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('presence', models.BooleanField(verbose_name='Guarani presence')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(verbose_name='name', max_length=512)),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='IndigenousLand',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('other_names', models.CharField(verbose_name='Others names', max_length=512)),
                ('official_area', models.FloatField(verbose_name='Official area')),
                ('guarani_exclusive_possession_area_portion', models.FloatField(null=True, blank=True, verbose_name='Guarani full and exclusive portion area possession')),
                ('others_exclusive_possession_area_portion', models.FloatField(null=True, blank=True, verbose_name='Others people full and exclusive portion area possession')),
                ('claim', models.TextField(null=True, blank=True, verbose_name='Clain')),
                ('demand', models.TextField(null=True, blank=True, verbose_name='Demand')),
                ('source', models.CharField(verbose_name='Source', max_length=512)),
                ('public_comments', models.TextField(null=True, blank=True, verbose_name='Comments')),
                ('private_comments', models.TextField(null=True, blank=True, verbose_name='Private comments')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(to='core.EthnicGroup', verbose_name='Ethnic group', related_name='indigenousland_ethnic_groups_layers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndigenousVillage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('other_names', models.CharField(verbose_name='Others names', max_length=512)),
                ('comments', models.TextField(null=True, blank=True, verbose_name='Comments')),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('population', models.CharField(null=True, blank=True, max_length=512)),
                ('guarani_presence', models.CharField(null=True, blank=True, max_length=512)),
                ('prominent_subgroup', models.CharField(null=True, blank=True, max_length=512)),
                ('ethnic_groups2', models.CharField(null=True, blank=True, verbose_name='Ethnic group', max_length=512)),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(to='core.EthnicGroup', verbose_name='Ethnic group', related_name='indigenousvillage_ethnic_groups_layers')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegalProceedings',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
                ('indigenous_land', models.ForeignKey(to='core.IndigenousLand', verbose_name='Guarani indigenous lands layer')),
                ('indigenous_village', models.ForeignKey(to='core.IndigenousVillage', verbose_name='Guarani indigenous villages layer')),
            ],
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('population', models.IntegerField(verbose_name='Population')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(verbose_name='name', max_length=512)),
                ('village', models.ForeignKey(verbose_name='Village', related_name='population_annual_series_population', to='core.IndigenousVillage')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='layer',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Layer', related_name='villages', to='core.MapLayer'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='layer',
            field=models.ForeignKey(verbose_name='Layer', related_name='indigenous_lads', to='core.MapLayer'),
        ),
        migrations.AddField(
            model_name='guaranipresence',
            name='village',
            field=models.ForeignKey(to='core.IndigenousVillage', verbose_name='Village'),
        ),
        migrations.AddField(
            model_name='documentation',
            name='type',
            field=models.ForeignKey(to='core.DocumentationType', verbose_name='type'),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='layer',
            field=models.ForeignKey(verbose_name='Layer', related_name='archaeological_places', to='core.MapLayer'),
        ),
    ]
