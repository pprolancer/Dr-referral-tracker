# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0015_auto_20160421_0940'),
    ]

    operations = [
        migrations.RenameModel('ClinicUserReportSetting',
                               'ClinicReportSetting'),
    ]
