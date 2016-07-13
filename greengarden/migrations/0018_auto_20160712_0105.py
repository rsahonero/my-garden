# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0017_auto_20160710_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='tratamiento',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='hecho',
            name='categoria',
            field=models.CharField(choices=[('F', 'Flor'), ('N', 'Ninguno'), ('R', 'Raiz'), ('T', 'Tallo'), ('H', 'Hoja')], default='N', max_length=1),
        ),
    ]