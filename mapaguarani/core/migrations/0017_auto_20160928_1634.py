# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_landtenurestatus_dashed_border'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionField',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('layers', models.ManyToManyField(blank=True, to='core.MapLayer', related_name='action_fields', verbose_name='Layers')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('address', models.CharField(max_length=512, null=True, verbose_name='address')),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='phone number')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='and date')),
                ('archaeological_places', models.ManyToManyField(blank=True, to='core.ArchaeologicalPlace', related_name='projects', verbose_name='Archaeological Place')),
                ('indigenous_lands', models.ManyToManyField(blank=True, to='core.IndigenousLand', related_name='projects', verbose_name='Indigenous Land')),
                ('indigenous_villages', models.ManyToManyField(blank=True, to='core.IndigenousVillage', related_name='projects', verbose_name='Indigenous Village')),
                ('layers', models.ManyToManyField(blank=True, to='core.MapLayer', related_name='projects', verbose_name='Layers')),
                ('organizations', models.ManyToManyField(blank=True, to='core.Organization', related_name='projects', verbose_name='Organization')),
            ],
        ),
        migrations.AddField(
            model_name='actionfield',
            name='organizations',
            field=models.ManyToManyField(blank=True, to='core.Organization', related_name='action_fields', verbose_name='Organization'),
        ),
        migrations.AddField(
            model_name='actionfield',
            name='projects',
            field=models.ManyToManyField(blank=True, to='core.Project', related_name='action_fields', verbose_name='Project'),
        ),
    ]
