# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150816_1914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indigenousland',
            old_name='document',
            new_name='documents',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='document',
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='position_source',
            field=models.CharField(verbose_name='Position Source', max_length=512),
        ),
    ]
