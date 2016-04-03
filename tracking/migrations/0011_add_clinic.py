# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0010_removing_patient_visit_record_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('creation_time', models.DateTimeField(verbose_name='Creation Timestamp', null=True, blank=True)),
                ('modification_time', models.DateTimeField(verbose_name='Modification Timestamp', null=True, blank=True)),
                ('clinic_name', models.CharField(verbose_name='Clinic Name', null=True, max_length=254, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
