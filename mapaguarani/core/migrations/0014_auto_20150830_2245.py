# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150818_2126'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='landtenurestatus',
            options={'verbose_name_plural': 'Land Tenures Status', 'verbose_name': 'Land Tenure Status'},
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='ethnic_groups',
            field=models.ManyToManyField(to='core.EthnicGroup', related_name='indigenousland_ethnic_groups_layers', blank=True, verbose_name='Ethnic group'),
        ),
    ]
