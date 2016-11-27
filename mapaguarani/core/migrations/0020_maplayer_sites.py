# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('core', '0019_auto_20161127_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
        ),
    ]
