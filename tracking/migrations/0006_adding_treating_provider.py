# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0005_refactor_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatingProvider',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('provider_name', models.CharField(max_length=254, unique=True, verbose_name='Name', null=True)),
                ('provider_title', models.CharField(blank=True, max_length=50, verbose_name='Title')),
                ('provider_type', models.CharField(blank=True, max_length=2, choices=[('PA', 'Physician Assistant'), ('D', 'Doctor'), ('N', 'Nurse'), ('NP', 'Nurse Practitioner')], verbose_name='Provider Type')),
            ],
        ),
        migrations.AlterField(
            model_name='organization',
            name='org_type',
            field=models.CharField(blank=True, max_length=3, choices=[('MAR', 'Marketing'), ('INS', 'Insurance'), ('INT', 'Internal'), ('WKC', 'Work comp.'), ('HCP', 'Healthcare Provider')], verbose_name='Group Type'),
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='treating_provider',
            field=models.ForeignKey(to='tracking.TreatingProvider', related_name='TreatingProvider', null=True, verbose_name='Referring Entity'),
        ),
    ]
