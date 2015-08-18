# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150816_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProminentEthnicSubGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Prominent Ethnic SubGroup',
                'verbose_name_plural': 'Prominent Ethnic SubGroups',
            },
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='prominent_subgroup',
            field=models.ManyToManyField(related_name='indigenousland_prominent_subgroup_layers', blank=True, verbose_name='prominent ethnic sub-group', to='core.ProminentEthnicSubGroup'),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='prominent_subgroup',
            field=models.ManyToManyField(related_name='indigenousvillage_prominent_subgroup_layers', blank=True, verbose_name='prominent ethnic sub-group', to='core.ProminentEthnicSubGroup'),
        ),
    ]
