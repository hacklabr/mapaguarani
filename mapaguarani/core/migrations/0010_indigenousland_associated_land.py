# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_indigenousland_associated_land'),
    ]

    operations = [
        migrations.AddField(
            model_name='indigenousland',
            name='associated_land',
            field=models.ForeignKey(null=True, verbose_name='Associated Land', blank=True, to='core.IndigenousLand'),
        ),
    ]
