# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-19 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20160819_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='num',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
