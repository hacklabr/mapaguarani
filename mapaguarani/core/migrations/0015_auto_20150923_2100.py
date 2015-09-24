# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150830_2245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archaeologicalplace',
            old_name='position',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='indigenousland',
            old_name='polygon',
            new_name='geometry',
        ),
        migrations.RenameField(
            model_name='indigenousvillage',
            old_name='position',
            new_name='geometry',
        ),
    ]
