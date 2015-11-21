# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150923_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='landtenurestatus',
            name='dashed_border',
            field=models.BooleanField(verbose_name='Dasshed border', default=False),
        ),
    ]
