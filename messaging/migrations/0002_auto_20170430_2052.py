# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 18:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('world', '0001_initial'),
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagerelationship',
            name='from_character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Character'),
        ),
        migrations.AddField(
            model_name='messagerelationship',
            name='to_character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_relationships_to', to='world.Character'),
        ),
        migrations.AddField(
            model_name='messagerecipientgroup',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.CharacterMessage'),
        ),
        migrations.AddField(
            model_name='messagerecipientgroup',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.Organization'),
        ),
        migrations.AddField(
            model_name='messagerecipient',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='world.Character'),
        ),
        migrations.AddField(
            model_name='messagerecipient',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='messaging.MessageRecipientGroup'),
        ),
        migrations.AddField(
            model_name='messagerecipient',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='messaging.CharacterMessage'),
        ),
        migrations.AddField(
            model_name='charactermessage',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages_sent', to='world.Character'),
        ),
        migrations.AlterUniqueTogether(
            name='messagerelationship',
            unique_together=set([('from_character', 'to_character')]),
        ),
        migrations.AlterUniqueTogether(
            name='messagerecipientgroup',
            unique_together=set([('message', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='messagerecipient',
            unique_together=set([('message', 'character')]),
        ),
        migrations.AlterIndexTogether(
            name='messagerecipient',
            index_together=set([('character', 'read')]),
        ),
    ]
