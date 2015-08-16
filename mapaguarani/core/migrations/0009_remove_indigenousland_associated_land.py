# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20150816_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indigenousland',
            name='associated_land',
        ),
    ]
