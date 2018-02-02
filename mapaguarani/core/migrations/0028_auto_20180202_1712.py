# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20180202_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legalprocedings',
            options={'verbose_name': 'Legal Proceding', 'verbose_name_plural': 'Legal Procedings'},
        ),
        migrations.RemoveField(
            model_name='legalprocedings',
            name='indigenous_land',
        ),
        migrations.AddField(
            model_name='legalprocedings',
            name='indigenous_land',
            field=models.ManyToManyField(verbose_name='Guarani indigenous lands layer', to='core.IndigenousLand'),
        ),
        migrations.RemoveField(
            model_name='legalprocedings',
            name='indigenous_village',
        ),
        migrations.AddField(
            model_name='legalprocedings',
            name='indigenous_village',
            field=models.ManyToManyField(verbose_name='Guarani indigenous villages layer', to='core.IndigenousVillage'),
        ),
    ]
