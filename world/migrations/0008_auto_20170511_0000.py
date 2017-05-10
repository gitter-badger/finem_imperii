# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-10 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0007_auto_20170507_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='settlement',
            name='guilds_setting',
            field=models.CharField(default='keep guilds', max_length=20),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='type',
            field=models.CharField(choices=[('grain', 'grain bushels'), ('cart', 'transport carts')], max_length=20),
        ),
    ]
