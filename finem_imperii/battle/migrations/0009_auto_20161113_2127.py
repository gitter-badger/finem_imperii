# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-11-13 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0008_battlecharacter_z'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battleunit',
            name='starting_x_pos',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='battleunit',
            name='starting_z_pos',
            field=models.IntegerField(default=0),
        ),
    ]
