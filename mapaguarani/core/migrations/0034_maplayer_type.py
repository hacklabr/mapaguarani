# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20180320_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='type',
            field=models.CharField(default='generic', verbose_name='Type', max_length=256, choices=[('village', 'Indigenous Village'), ('land', 'Indigenous Land'), ('archaeological', 'Archaeological Place'), ('generic', 'Generic')]),
        ),
    ]
