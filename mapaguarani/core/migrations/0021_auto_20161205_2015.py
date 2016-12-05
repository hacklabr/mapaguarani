# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_maplayer_sites'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255, blank=True, null=True)),
                ('desc', models.TextField(verbose_name='Description', blank=True, null=True)),
                ('credits', models.CharField(verbose_name='Credits (for photos)', max_length=512, blank=True, null=True)),
                ('type', models.CharField(choices=[('photo', 'Photo'), ('video', 'Video'), ('audio', 'Audio'), ('pdf', 'PDF'), ('others', 'Others')], default='video', verbose_name='Type', max_length=256)),
                ('file', models.FileField(verbose_name='File', upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectLink',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(verbose_name='Name', max_length=255, blank=True, null=True)),
                ('desc', models.TextField(verbose_name='Description', blank=True, null=True)),
                ('url', models.CharField(verbose_name='Link', max_length=512)),
                ('embed_code', models.TextField(verbose_name='Embed code', blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='files',
            field=models.ManyToManyField(verbose_name='Files', to='core.ProjectFile', blank=True, related_name='files'),
        ),
        migrations.AddField(
            model_name='project',
            name='links',
            field=models.ManyToManyField(verbose_name='Links (Youtube, instagram, etc)', to='core.ProjectLink', blank=True, related_name='links'),
        ),
    ]
