# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.migrations.operations import AddField, RemoveField
from django.utils import timezone

def forwards_func(apps, schema_editor):
    PatientVisit = apps.get_model("tracking", "PatientVisit")
    
    db_alias = schema_editor.connection.alias
    for visit in PatientVisit.objects.using(db_alias):
        visit.creation_time = visit.record_date
        visit.save()
        
def reverse_func(apps, schema_editor):
    PatientVisit = apps.get_model("tracking", "PatientVisit")

    db_alias = schema_editor.connection.alias
    for visit in PatientVisit.objects.using(db_alias):
        visit.record_date = visit.creation_time 
        visit.save()
 
    
class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0008_adding_creation_modification_time'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
