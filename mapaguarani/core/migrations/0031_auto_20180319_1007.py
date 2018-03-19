# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20180202_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guaranipresence',
            options={'get_latest_by': 'date', 'verbose_name': 'Indigenous Presence'},
        ),
        migrations.AlterField(
            model_name='guaranipresence',
            name='presence',
            field=models.BooleanField(verbose_name='Indigenous Presence'),
        ),
    ]
