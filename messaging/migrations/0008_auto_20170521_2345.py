# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-21 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0007_auto_20170518_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactermessage',
            name='category',
            field=models.CharField(blank=True, choices=[('travel', 'travel'), ('conquest', 'conquest'), ('turn', 'new turn'), ('proposal', 'action proposal'), ('battle', 'battle'), ('policy', 'policy and law'), ('ban', 'ban'), ('elections', 'elections'), ('diplomacy', 'diplomacy'), ('military stance', 'military stance'), ('battle formation', 'battle formation'), ('conquest', 'conquest'), ('guilds', 'conquest'), ('unit', 'unit'), ('welcome', 'welcome'), ('heir', 'heir'), ('leaving', 'leaving'), ('taxes', 'taxes')], max_length=20, null=True),
        ),
    ]
