# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0023_auto_20160719_0204'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HechosComparidos',
            new_name='CondicionesAtmosfericas',
        ),
        migrations.AlterField(
            model_name='hecho',
            name='categoria',
            field=models.CharField(choices=[('H', 'Hoja'), ('R', 'Raiz'), ('T', 'Tallo'), ('F', 'Flor'), ('N', 'Ninguno')], default='N', max_length=1),
        ),
    ]