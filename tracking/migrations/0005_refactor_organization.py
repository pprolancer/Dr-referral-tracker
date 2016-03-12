# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_changing_attributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='org_type',
            field=models.CharField(blank=True, max_length=2, verbose_name='Group Type', choices=[('MAR', 'Marketing'), ('INS', 'Insurance'), ('INT', 'Internal'), ('WKC', 'Work comp.'), ('HCP', 'Healthcare Provider')]),
        ),
    ]
