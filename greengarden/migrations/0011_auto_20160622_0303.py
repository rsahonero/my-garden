# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0010_auto_20160622_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hecho',
            name='reglas',
            field=models.ManyToManyField(blank=True, to='greengarden.Regla'),
        ),
    ]