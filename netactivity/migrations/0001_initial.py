# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('mac_address', models.CharField(unique=True, max_length=20)),
                ('last_ip_address', models.GenericIPAddressField(default=None, unique=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_ip_update', models.DateTimeField(default=None, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DNSElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(unique=True, max_length=255)),
                ('last_query', models.DateTimeField(default=None, null=True)),
                ('clients', models.ManyToManyField(to='netactivity.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NetSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port', models.PositiveIntegerField()),
                ('protocol', models.CharField(default=None, max_length=32, null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(to='netactivity.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TargetHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('reverse_dns', models.CharField(default=None, max_length=255, null=True)),
                ('location', models.CharField(default=None, max_length=2, null=True)),
                ('flag', models.CharField(max_length=32, choices=[(b'unknown', b'unknown'), (b'known', b'known'), (b'trusted', b'trusted'), (b'advertiser', b'advertiser'), (b'unwanted', b'unwanted'), (b'harmful', b'harmful')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='netsession',
            name='target_host',
            field=models.ForeignKey(to='netactivity.TargetHost'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dnselement',
            name='target_hosts',
            field=models.ManyToManyField(to='netactivity.TargetHost'),
            preserve_default=True,
        ),
    ]
