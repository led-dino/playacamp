# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-27 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_drop_transportation_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendanceprofile',
            name='housing_type_preference',
            field=models.CharField(blank=True, choices=[('campyurt', 'Camp Yurt'), ('personalyurt', 'Personal Yurt'), ('tent', 'Tent'), ('rv', 'RV'), ('container', 'Container'), ('other', 'Other'), ('van', 'Van'), ('shiftpod', 'Shiftpod')], max_length=10, null=True),
        ),
    ]
