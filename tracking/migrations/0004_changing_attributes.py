# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0003_renaming_models'),
    ]

    operations = [
        migrations.RenameField(
            model_name='referringentity',
            old_name='physician_email',
            new_name='entity_email',
        ),
        migrations.RenameField(
            model_name='referringentity',
            old_name='physician_phone',
            new_name='entity_phone',
        ),
        migrations.RenameField(
            model_name='referringentity',
            old_name='referral_special',
            new_name='entity_special',
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='visit_actual_time',
            field=models.TimeField(null=True, default=None, verbose_name='Actual Time'),
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='visit_appointment_time',
            field=models.TimeField(null=True, default=None, verbose_name='Appointment Time'),
        ),
        migrations.AddField(
            model_name='referringentity',
            name='entity_title',
            field=models.CharField(blank=True, max_length=50, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='record_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Record Date'),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='referring_entity',
            field=models.ForeignKey(to='tracking.ReferringEntity', verbose_name='Referring Entity', related_name='PatientVisit'),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='visit_count',
            field=models.IntegerField(default=1, verbose_name='Visit Count'),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='visit_date',
            field=models.DateField(default=datetime.date.today, verbose_name='Visit Date'),
        ),
        migrations.AlterField(
            model_name='referringentity',
            name='entity_name',
            field=models.CharField(null=True, max_length=254, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='referringentity',
            name='organization',
            field=models.ForeignKey(to='tracking.Organization', verbose_name='Group', related_name='ReferringEntity'),
        ),
        migrations.AlterField(
            model_name='thankyoumails',
            name='month_referrals',
            field=models.IntegerField(verbose_name='Month-PatientVisits'),
        ),
        migrations.AlterField(
            model_name='thankyoumails',
            name='year_referrals',
            field=models.IntegerField(verbose_name='Year-PatientVisits'),
        ),
    ]
