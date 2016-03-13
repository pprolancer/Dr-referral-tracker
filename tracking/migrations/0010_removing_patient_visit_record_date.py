# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0009_migrating_data_patient_visit_record_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientvisit',
            name='record_date',
        ),
    ]
