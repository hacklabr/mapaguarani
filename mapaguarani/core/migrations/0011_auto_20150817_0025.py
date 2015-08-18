# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_indigenousland_associated_land'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='population',
            options={'verbose_name_plural': 'Populations History', 'verbose_name': 'Population', 'get_latest_by': 'date'},
        ),
        migrations.AlterField(
            model_name='guaranipresence',
            name='village',
            field=models.ForeignKey(related_name='guarani_presence_annual_series', to='core.IndigenousVillage', verbose_name='Village'),
        ),
        migrations.AlterField(
            model_name='landtenure',
            name='map_color',
            field=models.CharField(max_length=64, blank=True, null=True, verbose_name='Color in Map'),
        ),
        migrations.AlterField(
            model_name='landtenurestatus',
            name='map_color',
            field=models.CharField(max_length=64, blank=True, null=True, verbose_name='Color in Map'),
        ),
        migrations.AlterField(
            model_name='population',
            name='village',
            field=models.ForeignKey(related_name='population_annual_series', to='core.IndigenousVillage', verbose_name='Village'),
        ),
    ]
