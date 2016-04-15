# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0013_auto_20160412_1228'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicUserReportSetting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('creation_time', models.DateTimeField(verbose_name='Creation Timestamp', null=True, blank=True)),
                ('modification_time', models.DateTimeField(verbose_name='Modification Timestamp', null=True, blank=True)),
                ('enabled', models.BooleanField(verbose_name='Enabled', default=True)),
                ('period', models.CharField(max_length=16, verbose_name='Report Period', default='daily', choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')])),
                ('report_name', models.CharField(max_length=64, verbose_name='Report Name', choices=[('visit_history', 'visit_history')])),
                ('clinic_user', models.ForeignKey(to='tracking.ClinicUser')),
            ],
        ),
        migrations.AlterField(
            model_name='referringreportsetting',
            name='enabled',
            field=models.BooleanField(verbose_name='Enabled', default=True),
        ),
        migrations.AlterField(
            model_name='referringreportsetting',
            name='report_name',
            field=models.CharField(max_length=64, verbose_name='Report Name', choices=[('thankyou', 'thankyou')]),
        ),
        migrations.AlterUniqueTogether(
            name='clinicuserreportsetting',
            unique_together=set([('clinic_user', 'report_name')]),
        ),
    ]
