# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0012_hecho_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hecho',
            name='titulo',
            field=models.CharField(default='', max_length=150),
        ),
    ]
