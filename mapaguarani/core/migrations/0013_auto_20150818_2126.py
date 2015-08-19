# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150817_0139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='biblio_references',
            field=models.CharField(verbose_name='Source', max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='cnsa',
            field=models.CharField(verbose_name='CNSA', max_length=512, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='code',
            field=models.CharField(verbose_name='Code', max_length=255, null=True, blank=True),
        ),
    ]
