# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netactivity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dnselement',
            name='type',
            field=models.CharField(default=b'A', max_length=5),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dnselement',
            name='domain',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='dnselement',
            unique_together=set([(b'domain', b'type')]),
        ),
    ]
