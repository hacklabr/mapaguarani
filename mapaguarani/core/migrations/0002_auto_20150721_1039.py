# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indigenousland',
            name='ethnic_groups',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='ethnic_groups2',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='guarani_presence',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='population',
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='associated_land',
            field=models.CharField(blank=True, verbose_name='Source', null=True, max_length=512),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='land_tenure',
            field=models.CharField(verbose_name='Land Tenure', choices=[('no_arrangements', 'Sem Providências'), ('regularized', 'Regularizada'), ('expropriated', 'Desapropriada'), ('expropriated_in_progress', 'Em processo de desapropriação'), ('delimited', 'Delimitada'), ('study', 'Em estudo'), ('declared', 'Declarada'), ('acquired', 'Adquirida'), ('regularized_limits_rev', 'Regularizada (Em revisão de limites)')], null=True, max_length=256),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='land_tenure_status',
            field=models.CharField(blank=True, verbose_name='Land Tenure Status', choices=[('no_revision', 'No Revision'), ('not_delimited', 'Not Delimited'), ('revised_land', 'Revised Land'), ('original_land', 'Original Land')], max_length=256),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='prominent_subgroup',
            field=models.ManyToManyField(blank=True, verbose_name='prominent ethnic sub-group', to='core.EthnicGroup', related_name='indigenousland_prominent_subgroup_layers'),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='position_precision',
            field=models.CharField(verbose_name='Land Tenure', choices=[('exact', 'Exact'), ('approximate', 'Approximate'), ('no_info', 'No information')], default='no_info', max_length=256),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='position_source',
            field=models.CharField(blank=True, verbose_name='Source', max_length=512),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='private_comments',
            field=models.TextField(blank=True, verbose_name='Private comments', null=True),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='public_comments',
            field=models.TextField(blank=True, verbose_name='Comments', null=True),
        ),
        migrations.AlterField(
            model_name='guaranipresence',
            name='village',
            field=models.ForeignKey(verbose_name='Village', to='core.IndigenousVillage', related_name='guaranipresence_annual_series_guarani_presence'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='documentation',
            field=models.ManyToManyField(blank=True, verbose_name='documentation', to='core.Documentation', related_name='indigenousland_documentation'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='documentation',
            field=models.ManyToManyField(blank=True, verbose_name='documentation', to='core.Documentation', related_name='indigenousvillage_documentation'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='ethnic_groups',
            field=models.ManyToManyField(blank=True, verbose_name='Ethnic group', to='core.EthnicGroup', related_name='indigenousvillage_ethnic_groups_layers'),
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='prominent_subgroup',
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='prominent_subgroup',
            field=models.ManyToManyField(blank=True, verbose_name='prominent ethnic sub-group', to='core.EthnicGroup', related_name='indigenousvillage_prominent_subgroup_layers'),
        ),
        migrations.AlterField(
            model_name='population',
            name='source',
            field=models.CharField(verbose_name='Source', max_length=512),
        ),
    ]
