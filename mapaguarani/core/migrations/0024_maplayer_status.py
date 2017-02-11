# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170209_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='maplayer',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted')], max_length=256, verbose_name='Status', default='restricted'),
        ),
    ]
