# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0028_auto_20170316_2311'),
        ('organization', '0023_organization_next_election'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Character')),
            ],
        ),
        migrations.CreateModel(
            name='PositionElection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.IntegerField()),
                ('closed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='PositionElectionVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.PositionCandidate')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.PositionElection')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Character')),
            ],
        ),
        migrations.RemoveField(
            model_name='organization',
            name='next_election',
        ),
        migrations.AlterField(
            model_name='capability',
            name='type',
            field=models.CharField(choices=[('ban', 'ban'), ('policy', 'write policy and law'), ('diplomacy', 'diplomacy'), ('conscript', 'conscript troops'), ('dissolve', 'dissolve'), ('suborganizations', 'manage subordinate organizations'), ('secede', 'secede'), ('memberships', 'memberships'), ('heir', 'set heir'), ('elect', 'elect'), ('candidacy', 'present candidacy'), ('convoke elections', 'convoke elections')], max_length=20),
        ),
        migrations.AddField(
            model_name='positionelection',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='positionelection',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.PositionCandidate'),
        ),
        migrations.AddField(
            model_name='positioncandidate',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
    ]