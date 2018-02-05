# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20180202_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indigenousland',
            name='claim',
            field=models.TextField(blank=True, verbose_name='Claim', null=True),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='ethnic_groups',
            field=models.ManyToManyField(related_name='indigenousland_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='Ethnic group'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='land_tenure',
            field=models.ForeignKey(to='core.LandTenure', related_name='indigenous_lands', verbose_name='Land Tenure'),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='land_tenure_status',
            field=models.ForeignKey(to='core.LandTenureStatus', related_name='indigenous_lands', verbose_name='Land Tenure Status'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='ethnic_groups',
            field=models.ManyToManyField(related_name='indigenousvillage_ethnic_groups_layers', to='core.EthnicGroup', verbose_name='Ethnic group'),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='layer',
            field=models.ForeignKey(to='core.MapLayer', related_name='villages', verbose_name='Layer'),
        ),
    ]
