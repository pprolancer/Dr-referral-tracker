# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0006_adding_treating_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvisit',
            name='treating_provider',
            field=models.ForeignKey(verbose_name='Treating Provider', to='tracking.TreatingProvider', related_name='TreatingProvider', null=True),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='visit_actual_time',
            field=models.TimeField(blank=True, default=None, verbose_name='Actual Time', null=True),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='visit_appointment_time',
            field=models.TimeField(blank=True, default=None, verbose_name='Appointment Time', null=True),
        ),
    ]
