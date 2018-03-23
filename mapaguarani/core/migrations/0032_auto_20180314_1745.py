# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0031_auto_20180306_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maplayer',
            name='creation_groups',
        ),
        migrations.RemoveField(
            model_name='maplayer',
            name='edition_groups',
        ),
        migrations.AddField(
            model_name='maplayer',
            name='permission_groups',
            field=models.ManyToManyField(to='auth.Group', related_name='_maplayer_permission_groups_+'),
        ),
    ]
