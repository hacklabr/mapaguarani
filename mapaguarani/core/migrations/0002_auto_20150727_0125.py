# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(verbose_name='name', max_length=255)),
                ('file', models.FileField(upload_to='', verbose_name='attached file')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(null=True, blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'Indigenous Place Documents',
                'verbose_name': 'Indigenous Place Document',
            },
        ),
        migrations.RenameModel(
            old_name='DocumentationType',
            new_name='DocumentType',
        ),
        migrations.RemoveField(
            model_name='documentation',
            name='type',
        ),
        migrations.AlterModelOptions(
            name='archaeologicalplace',
            options={'verbose_name_plural': 'Archaeological Places', 'verbose_name': 'Archaeological Place'},
        ),
        migrations.AlterModelOptions(
            name='documenttype',
            options={'verbose_name_plural': 'Indigenous Place Document Types', 'verbose_name': 'Indigenous Place Document Type'},
        ),
        migrations.AlterModelOptions(
            name='ethnicgroup',
            options={'verbose_name_plural': 'Ethnic Groups', 'verbose_name': 'Ethnic Group'},
        ),
        migrations.AlterModelOptions(
            name='guaranipresence',
            options={'verbose_name': 'Guarani Presence', 'get_latest_by': 'date'},
        ),
        migrations.AlterModelOptions(
            name='indigenousland',
            options={'verbose_name_plural': 'Indigenous Lands', 'verbose_name': 'Indigenous Land'},
        ),
        migrations.AlterModelOptions(
            name='indigenousvillage',
            options={'verbose_name_plural': 'Indigenous Villages', 'verbose_name': 'Indigenous Village'},
        ),
        migrations.AlterModelOptions(
            name='legalproceedings',
            options={'verbose_name_plural': 'Legal Proceedings', 'verbose_name': 'Legal Proceeding'},
        ),
        migrations.AlterModelOptions(
            name='maplayer',
            options={'verbose_name_plural': 'Map Layers', 'verbose_name': 'Map Layer'},
        ),
        migrations.AlterModelOptions(
            name='population',
            options={'verbose_name_plural': 'Populations', 'verbose_name': 'Population', 'get_latest_by': 'date'},
        ),
        migrations.RemoveField(
            model_name='indigenousland',
            name='documentation',
        ),
        migrations.RemoveField(
            model_name='indigenousvillage',
            name='documentation',
        ),
        migrations.DeleteModel(
            name='Documentation',
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(verbose_name='type', to='core.DocumentType'),
        ),
        migrations.AddField(
            model_name='indigenousland',
            name='document',
            field=models.ManyToManyField(verbose_name='documentation', blank=True, to='core.Document', related_name='indigenousland_documentation'),
        ),
        migrations.AddField(
            model_name='indigenousvillage',
            name='document',
            field=models.ManyToManyField(verbose_name='documentation', blank=True, to='core.Document', related_name='indigenousvillage_documentation'),
        ),
    ]
