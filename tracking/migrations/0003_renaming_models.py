# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.db.migrations.operations import RenameModel, RenameField, AlterField
from tracking.models import ReferringEntity  


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0002_referral_referral_date'),
    ]

    operations = [
        RenameModel("Physician", "ReferringEntity"),
        RenameField("ReferringEntity", "physician_name", "entity_name"),
        RenameModel("Referral", "PatientVisit"),
        RenameField("PatientVisit", "referral_date", "record_date"),      
        RenameField("PatientVisit", "physician", "referring_entity"),      
        AlterField("PatientVisit", "referring_entity", models.ForeignKey(
                                                  ReferringEntity, 
                                                  related_name="PatientVisit",
                                                  verbose_name="Practitioner")), 
        RenameField("ThankyouMails", "physician", "referring_entity"),
        AlterField("ThankyouMails", "referring_entity", models.ForeignKey(
                                                 ReferringEntity, 
                                                 related_name="thankyou_mail")), 
    ]
