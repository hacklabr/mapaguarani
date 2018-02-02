# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_remove_archaeologicalplace_code'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LegalProceedings',
            new_name='LegalProcedings',
        ),
        migrations.AlterField(
            model_name='landtenurestatus',
            name='dashed_border',
            field=models.BooleanField(verbose_name='Dashed border', default=False),
        ),
    ]
