# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20150816_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indigenousland',
            name='land_tenure',
        ),
        migrations.RemoveField(
            model_name='indigenousland',
            name='land_tenure_status',
        ),
    ]
