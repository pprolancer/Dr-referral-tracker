# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referral',
            name='referral_date',
            field=models.DateTimeField(verbose_name='Referral Date', default=django.utils.timezone.now),
        ),
    ]
