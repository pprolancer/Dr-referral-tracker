# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('month', models.IntegerField(verbose_name='month')),
                ('year', models.IntegerField(verbose_name='year')),
                ('is_sent', models.BooleanField(verbose_name='sent', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('org_name', models.CharField(verbose_name='Group Name', null=True, unique=True, max_length=254)),
                ('org_contact_name', models.CharField(verbose_name='Contact name', null=True, blank=True, max_length=254)),
                ('org_phone', phonenumber_field.modelfields.PhoneNumberField(verbose_name='Phone', blank=True, max_length=128)),
                ('org_email', models.EmailField(verbose_name='Email address', blank=True, max_length=254)),
                ('org_special', models.BooleanField(verbose_name='Special type', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('physician_name', models.CharField(verbose_name='Practitioner Name', null=True, unique=True, max_length=254)),
                ('physician_phone', phonenumber_field.modelfields.PhoneNumberField(verbose_name='Phone', blank=True, max_length=128)),
                ('physician_email', models.EmailField(verbose_name='Email address', blank=True, max_length=254)),
                ('referral_special', models.BooleanField(verbose_name='Special type', default=False)),
                ('organization', models.ForeignKey(verbose_name='Group', related_name='Physician', to='tracking.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('visit_date', models.DateField(verbose_name='Date', default=datetime.date.today)),
                ('visit_count', models.IntegerField(verbose_name='Referrals', default=1)),
                ('physician', models.ForeignKey(verbose_name='Practitioner', related_name='Referral', to='tracking.Physician')),
            ],
        ),
        migrations.CreateModel(
            name='ThankyouMails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('month_referrals', models.IntegerField(verbose_name='Month-Referrals')),
                ('year_referrals', models.IntegerField(verbose_name='Year-Referrals')),
                ('active', models.BooleanField(verbose_name='approve', default=False)),
                ('emailreport', models.ForeignKey(related_name='email_report', default=1, to='tracking.EmailReport')),
                ('physician', models.ForeignKey(related_name='thankyou_mail', to='tracking.Physician')),
            ],
        ),
    ]
