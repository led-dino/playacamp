# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-14 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20180530_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='max_size',
            field=models.IntegerField(default=1),
        ),
    ]