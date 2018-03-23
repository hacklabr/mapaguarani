# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20180314_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maplayer',
            name='permission_groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
