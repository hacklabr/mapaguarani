# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150727_0157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indigenousland',
            name='prominent_subgroup',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='prominent_subgroup',
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='position_precision',
            field=models.CharField(max_length=256, choices=[('exact', 'Exact'), ('approximate', 'Approximate'), ('no_info', 'No information')], verbose_name='Position Precision', default='no_info'),
        ),
    ]
