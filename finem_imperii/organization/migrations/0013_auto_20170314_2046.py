# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-14 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_auto_20170314_1957'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='policydocumentversion',
            name='document',
        ),
        migrations.RemoveField(
            model_name='policydocument',
            name='active',
        ),
        migrations.AddField(
            model_name='policydocument',
            name='body',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PolicyDocumentVersion',
        ),
    ]
