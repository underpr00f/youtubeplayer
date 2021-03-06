# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-12 21:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0009_auto_20170804_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberAccept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agree', models.BooleanField()),
                ('accepter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepteruser', to=settings.AUTH_USER_MODEL)),
                ('acceptroom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acceptroom', to='chat.Member')),
            ],
        ),
    ]
