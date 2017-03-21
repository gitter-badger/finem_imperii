# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_auto_20170321_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capability',
            name='type',
            field=models.CharField(choices=[('ban', 'ban'), ('policy', 'write policy and law'), ('diplomacy', 'diplomacy'), ('conscript', 'conscript troops'), ('dissolve', 'dissolve'), ('suborganizations', 'manage subordinate organizations'), ('secede', 'secede'), ('memberships', 'memberships'), ('heir', 'set heir'), ('elect', 'elect')], max_length=15),
        ),
    ]