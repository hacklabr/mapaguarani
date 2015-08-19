# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150817_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchaeologicalImage',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(null=True, verbose_name='name', blank=True, max_length=255)),
                ('desc', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('credits', models.CharField(null=True, verbose_name='Credits', blank=True, max_length=512)),
                ('image', models.ImageField(verbose_name='Image', upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='biblio_references',
            field=models.CharField(null=True, verbose_name='Acronym', blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='cnsa',
            field=models.CharField(null=True, verbose_name='Acronym', blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='code',
            field=models.CharField(null=True, verbose_name='name', blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='archaeologicalplace',
            name='position',
            field=django.contrib.gis.db.models.fields.PointField(default=0, srid=4326),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='archaeologicalplace',
            name='acronym',
            field=models.CharField(null=True, verbose_name='Acronym', blank=True, max_length=512),
        ),
        migrations.AddField(
            model_name='archaeologicalimage',
            name='archaeological_place',
            field=models.ForeignKey(related_name='images', verbose_name='Archaeological Place', to='core.ArchaeologicalPlace'),
        ),
    ]
