# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160928_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='archaeologicalplace',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted')], default='restricted', max_length=256, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted')], default='restricted', max_length=256, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('restricted', 'Restricted')], default='restricted', max_length=256, verbose_name='Status'),
        ),
    ]
