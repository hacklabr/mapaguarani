# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0030_auto_20180202_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='creation_groups',
            field=models.ManyToManyField(related_name='_maplayer_creation_groups_+', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='maplayer',
            name='edition_groups',
            field=models.ManyToManyField(related_name='_maplayer_edition_groups_+', to='auth.Group'),
        ),
    ]
