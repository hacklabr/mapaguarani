# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_maplayer_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='archaeologicalplace',
            name='ap_date',
            field=models.CharField(null=True, blank=True, verbose_name='ap date', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='calibrated_dating',
            field=models.CharField(null=True, blank=True, verbose_name='calibrated dating', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='chrono_ref',
            field=models.CharField(null=True, blank=True, verbose_name='chronological reference', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='dating',
            field=models.CharField(null=True, blank=True, verbose_name='dating', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='dating_method',
            field=models.CharField(null=True, blank=True, verbose_name='dating method', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='deviation',
            field=models.CharField(null=True, blank=True, verbose_name='deviation', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='hydrography',
            field=models.CharField(null=True, blank=True, verbose_name='hydrography', max_length=512),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='institution',
            field=models.CharField(null=True, blank=True, verbose_name='institution', max_length=512),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='lab_code',
            field=models.CharField(null=True, blank=True, verbose_name='laboratory code', max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='phase',
            field=models.CharField(null=True, blank=True, verbose_name='phase', max_length=255),
        ),
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='position_precision',
            field=models.CharField(choices=[('exact', 'Exact'), ('approximate', 'Approximate'), ('by_city', 'By City'), ('no_position', 'No position')], verbose_name='Position Precision', max_length=128),
        ),
    ]
