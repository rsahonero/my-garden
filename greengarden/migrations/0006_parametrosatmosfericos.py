# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-24 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0005_auto_20160823_0423'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametrosAtmosfericos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=4)),
                ('humedad_relativa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('mes', models.CharField(max_length=50)),
            ],
        ),
    ]