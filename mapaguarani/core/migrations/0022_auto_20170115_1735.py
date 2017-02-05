# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20161205_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectlink',
            name='type',
            field=models.CharField(verbose_name='Type', max_length=256, default='vimeo', choices=[('youtube', 'youtube'), ('vimeo', 'vimeo'), ('flickr', 'flickr'), ('instagram', 'instagram'), ('others', 'Others')]),
        ),
        migrations.AlterField(
            model_name='guaranipresence',
            name='source',
            field=models.CharField(max_length=512, verbose_name='Source'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
