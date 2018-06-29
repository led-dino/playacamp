# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-17 19:38
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import F


def copy_transportation_method(apps, schema_editor):
    MyModel = apps.get_model('main', 'attendanceprofile')
    MyModel.objects.all().update(to_transportation_method=F('transportation_method'))
    MyModel.objects.all().update(from_transportation_method=F('transportation_method'))


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_add_to_from_transportation_method'),
    ]

    operations = [
        migrations.RunPython(copy_transportation_method),
    ]