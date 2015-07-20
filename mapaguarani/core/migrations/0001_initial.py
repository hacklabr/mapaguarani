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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('acronym', models.CharField(verbose_name='name', max_length=512)),
                ('position_precision', models.CharField(verbose_name='Position Precision', max_length=128, choices=[('exact', 'Exact'), ('estimated', 'Estimated'), ('by_city', 'By City'), ('no_position', 'No position')])),
                ('position_comments', models.TextField(verbose_name='Position Comments')),
            ],
        ),
        migrations.CreateModel(
            name='Documentation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('file', models.FileField(verbose_name='attached file', upload_to='')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(verbose_name='description', blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EthnicGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GuaraniPresence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('other_names', models.CharField(verbose_name='Others names', max_length=512)),
                ('public_comments', models.TextField(verbose_name='Comments', blank=True, null=True)),
                ('private_comments', models.TextField(verbose_name='Private comments', blank=True, null=True)),
                ('official_area', models.FloatField(verbose_name='Official area')),
                ('guarani_exclusive_possession_area_portion', models.FloatField(verbose_name='Guarani full and exclusive portion area possession', blank=True, null=True)),
                ('others_exclusive_possession_area_portion', models.FloatField(verbose_name='Others people full and exclusive portion area possession', blank=True, null=True)),
                ('claim', models.TextField(verbose_name='Clain', blank=True, null=True)),
                ('demand', models.TextField(verbose_name='Demand', blank=True, null=True)),
                ('source', models.CharField(verbose_name='Source', max_length=512)),
                ('land_tenure', models.CharField(verbose_name='Land Tenure', max_length=256, choices=[('no_arrangements', 'Sem Providências'), ('regularized', 'Regularizada'), ('expropriated', 'Desapropriada'), ('expropriated_in_progress', 'Em processo de desapropriação'), ('delimited', 'Delimitada'), ('study', 'Em estudo'), ('declared', 'Declarada'), ('acquired', 'Adquirida'), ('regularized_limits_rev', 'Regularizada (Em revisão de limites)')])),
                ('land_tenure_status', models.CharField(verbose_name='Land Tenure Status', max_length=256, choices=[('no_revision', 'No Revision'), ('not_delimited', 'Not Delimited'), ('revised_land', 'Revised Land'), ('original_land', 'Original Land')])),
                ('associated_land', models.CharField(verbose_name='Source', max_length=512, blank=True, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('documentation', models.ManyToManyField(verbose_name='documentation', blank=True, related_name='indigenousland_documentation', to='core.Documentation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IndigenousVillage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('other_names', models.CharField(verbose_name='Others names', max_length=512)),
                ('public_comments', models.TextField(verbose_name='Comments', blank=True, null=True)),
                ('private_comments', models.TextField(verbose_name='Private comments', blank=True, null=True)),
                ('comments', models.TextField(verbose_name='Comments', blank=True, null=True)),
                ('position_precision', models.CharField(verbose_name='Land Tenure', max_length=256, choices=[('exact', 'Exact'), ('approximate', 'Approximate'), ('no_info', 'No information')], default='no_info')),
                ('position_source', models.CharField(verbose_name='Source', max_length=512)),
                ('position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('documentation', models.ManyToManyField(verbose_name='documentation', blank=True, related_name='indigenousvillage_documentation', to='core.Documentation')),
                ('ethnic_groups', models.ManyToManyField(verbose_name='Ethnic group', blank=True, related_name='indigenousvillage_ethnic_groups_layers', to='core.EthnicGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LegalProceedings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
                ('indigenous_land', models.ForeignKey(verbose_name='Guarani indigenous lands layer', to='core.IndigenousLand')),
                ('indigenous_village', models.ForeignKey(verbose_name='Guarani indigenous villages layer', to='core.IndigenousVillage')),
            ],
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('population', models.IntegerField(verbose_name='Population')),
                ('date', models.DateField(verbose_name='Date')),
                ('source', models.CharField(verbose_name='Source', max_length=512)),
                ('village', models.ForeignKey(verbose_name='Village', to='core.IndigenousVillage', related_name='population_annual_series_population')),
            ],
            options={
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='layer',
            field=models.ForeignKey(to='core.MapLayer', null=True, verbose_name='Layer', blank=True, related_name='villages'),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='prominent_subgroup',
            field=models.ManyToManyField(verbose_name='prominent ethnic sub-group', blank=True, related_name='indigenousvillage_prominent_subgroup_layers', to='core.EthnicGroup'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='layer',
            field=models.ForeignKey(verbose_name='Layer', to='core.MapLayer', related_name='indigenous_lads'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='prominent_subgroup',
            field=models.ManyToManyField(verbose_name='prominent ethnic sub-group', blank=True, related_name='indigenousland_prominent_subgroup_layers', to='core.EthnicGroup'),
        ),
        migrations.AddField(
            model_name='guaranipresence',
            name='village',
            field=models.ForeignKey(verbose_name='Village', to='core.IndigenousVillage', related_name='guaranipresence_annual_series_guarani_presence'),
        ),
        migrations.AddField(
            model_name='documentation',
            name='type',
            field=models.ForeignKey(verbose_name='type', to='core.DocumentationType'),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='layer',
            field=models.ForeignKey(verbose_name='Layer', to='core.MapLayer', related_name='archaeological_places'),
        ),
    ]
