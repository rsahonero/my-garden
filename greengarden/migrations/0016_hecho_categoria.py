# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0015_auto_20160703_0312'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho',
            name='categoria',
            field=models.CharField(choices=[('R', 'Raiz'), ('H', 'Hoja'), ('N', 'Ninguno'), ('T', 'Tallo'), ('F', 'Flor')], default='N', max_length=1),
        ),
    ]