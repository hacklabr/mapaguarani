# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20170820_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archaeologicalplace',
            name='code',
        ),
    ]
