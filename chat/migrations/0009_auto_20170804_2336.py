# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-04 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20170804_2334'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'verbose_name': 'Приватная комната'},
        ),
        migrations.AlterField(
            model_name='member',
            name='label',
            field=models.SlugField(unique=True, verbose_name='Название'),
        ),
    ]
