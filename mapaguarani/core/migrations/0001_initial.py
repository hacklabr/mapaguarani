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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('acronym', models.CharField(max_length=512, verbose_name='name')),
                ('position_precision', models.CharField(choices=[('exact', 'Exact'), ('estimated', 'Estimated'), ('by_city', 'By City'), ('no_position', 'No position')], max_length=128, verbose_name='Position Precision')),
                ('position_comments', models.TextField(verbose_name='Position Comments')),
            ],
        ),
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('file', models.FileField(upload_to='', verbose_name='attached file')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentationType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='GuaraniPresence',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('presence', models.BooleanField(verbose_name='Guarani presence')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(max_length=512, verbose_name='name')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='IndigenousLand',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('other_names', models.CharField(max_length=512, verbose_name='Others names')),
                ('official_area', models.FloatField(verbose_name='Official area')),
                ('guarani_exclusive_possession_area_portion', models.FloatField(blank=True, null=True, verbose_name='Guarani full and exclusive portion area possession')),
                ('others_exclusive_possession_area_portion', models.FloatField(blank=True, null=True, verbose_name='Others people full and exclusive portion area possession')),
                ('claim', models.TextField(blank=True, null=True, verbose_name='Clain')),
                ('demand', models.TextField(blank=True, null=True, verbose_name='Demand')),
                ('source', models.CharField(max_length=512, verbose_name='Source')),
                ('public_comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('private_comments', models.TextField(blank=True, null=True, verbose_name='Private comments')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(related_name='indigenousland_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='Ethnic group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndigenousVillage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('other_names', models.CharField(max_length=512, verbose_name='Others names')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='Comments')),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('population', models.CharField(blank=True, null=True, max_length=512)),
                ('guarani_presence', models.CharField(blank=True, null=True, max_length=512)),
                ('prominent_subgroup', models.CharField(blank=True, null=True, max_length=512)),
                ('ethnic_groups2', models.CharField(blank=True, null=True, max_length=512, verbose_name='Ethnic group')),
                ('documentation', models.ManyToManyField(to='core.Documentation', verbose_name='documentation')),
                ('ethnic_groups', models.ManyToManyField(related_name='indigenousvillage_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='Ethnic group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegalProceedings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='Description')),
                ('indigenous_land', models.ForeignKey(to='core.IndigenousLand', verbose_name='Guarani indigenous lands layer')),
                ('indigenous_village', models.ForeignKey(to='core.IndigenousVillage', verbose_name='Guarani indigenous villages layer')),
            ],
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('population', models.IntegerField(verbose_name='Population')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(max_length=512, verbose_name='name')),
                ('village', models.ForeignKey(related_name='population_annual_series_population', to='core.IndigenousVillage', verbose_name='Village')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='layer',
            field=models.ForeignKey(blank=True, related_name='villages', null=True, to='core.MapLayer', verbose_name='Layer'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='layer',
            field=models.ForeignKey(related_name='indigenous_lads', to='core.MapLayer', verbose_name='Layer'),
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
            field=models.ForeignKey(related_name='archaeological_places', to='core.MapLayer', verbose_name='Layer'),
        ),
    ]
