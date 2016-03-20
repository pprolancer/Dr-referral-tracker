# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0012_create_link_to_clinic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clinic',
            old_name='name',
            new_name='clinic_name',
        ),
    ]
