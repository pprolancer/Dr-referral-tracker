# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0007_auto_20160313_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='creation_time',
            field=models.DateTimeField(blank=True, verbose_name='Creation Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='modification_time',
            field=models.DateTimeField(blank=True, verbose_name='Modification Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='creation_time',
            field=models.DateTimeField(blank=True, verbose_name='Creation Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='modification_time',
            field=models.DateTimeField(blank=True, verbose_name='Modification Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='referringentity',
            name='creation_time',
            field=models.DateTimeField(blank=True, verbose_name='Creation Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='referringentity',
            name='modification_time',
            field=models.DateTimeField(blank=True, verbose_name='Modification Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='treatingprovider',
            name='creation_time',
            field=models.DateTimeField(blank=True, verbose_name='Creation Timestamp', null=True),
        ),
        migrations.AddField(
            model_name='treatingprovider',
            name='modification_time',
            field=models.DateTimeField(blank=True, verbose_name='Modification Timestamp', null=True),
        ),
    ]
