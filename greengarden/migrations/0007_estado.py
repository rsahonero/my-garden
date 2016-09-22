# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-17 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greengarden', '0006_parametrosatmosfericos'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('imagen', models.CharField(max_length=100)),
                ('codigo', models.CharField(choices=[('AS', 'Controlado'), ('RS', 'Riesgo'), ('IN', 'Infectado')], max_length=2)),
            ],
        ),
    ]
