# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20161127_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='status',
            field=models.CharField(max_length=256, default='restricted', verbose_name='Status', choices=[('public', 'Public'), ('restricted', 'Restricted')]),
        ),
        migrations.AlterField(
            model_name='indigenousland',
            name='status',
            field=models.CharField(max_length=256, default='restricted', verbose_name='Status', choices=[('public', 'Public'), ('restricted', 'Restricted')]),
        ),
        migrations.AlterField(
            model_name='indigenousvillage',
            name='status',
            field=models.CharField(max_length=256, default='restricted', verbose_name='Status', choices=[('public', 'Public'), ('restricted', 'Restricted')]),
        ),
    ]
