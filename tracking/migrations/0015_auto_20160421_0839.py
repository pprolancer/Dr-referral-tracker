# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import tracking.middlewares
from tracking.models import Clinic
try:
    tracking.middlewares._set_current_clinic(
        Clinic.objects.order_by('id').first())
except:
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0014_auto_20160415_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinicuserreportsetting',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='patientvisit',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='referringentity',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AddField(
            model_name='referringreportsetting',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AlterField(
            model_name='clinic',
            name='clinic_name',
            field=models.CharField(max_length=254, default='main', unique=True, verbose_name='Clinic Name'),
        ),
        migrations.AlterField(
            model_name='clinicuser',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
        migrations.AlterField(
            model_name='treatingprovider',
            name='clinic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=tracking.middlewares.get_current_clinic_id, to='tracking.Clinic', null=True),
        ),
    ]
