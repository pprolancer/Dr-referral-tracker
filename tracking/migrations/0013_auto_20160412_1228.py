# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0012_create_link_to_clinic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferringReportSetting',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('creation_time', models.DateTimeField(verbose_name='Creation Timestamp', blank=True, null=True)),
                ('modification_time', models.DateTimeField(verbose_name='Modification Timestamp', blank=True, null=True)),
                ('report_name', models.CharField(choices=[('visit_history', 'visit_history'), ('thankyou', 'thankyou')], verbose_name='Report Name', max_length=64)),
                ('enabled', models.BooleanField(verbose_name='Special type', default=True)),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')], verbose_name='Report Period', default='daily', max_length=16)),
                ('referring_entity', models.ForeignKey(to='tracking.ReferringEntity')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='referringreportsetting',
            unique_together=set([('referring_entity', 'report_name')]),
        ),
        migrations.AlterField(
            model_name='patientvisit',
            name='visit_count',
            field=models.PositiveIntegerField(default=1, verbose_name='Visit Count', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.DeleteModel(
            name='ThankyouMails',
        ),
        migrations.DeleteModel(
            name='EmailReport',
        ),
    ]
