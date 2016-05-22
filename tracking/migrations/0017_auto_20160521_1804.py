# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0016_auto_20160424_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='org_name',
            field=models.CharField(max_length=254, verbose_name='Group Name', unique=True),
        ),
    ]
