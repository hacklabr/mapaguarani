# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20180202_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indigenousland',
            name='others_exclusive_possession_area_portion',
            field=models.FloatField(blank=True, null=True, verbose_name="Other peoples' full and exclusive portion area possession"),
        ),
    ]
