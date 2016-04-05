# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0011_add_clinic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinicUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('creation_time', models.DateTimeField(blank=True, verbose_name='Creation Timestamp', null=True)),
                ('modification_time', models.DateTimeField(blank=True, verbose_name='Modification Timestamp', null=True)),
                ('clinic', models.ForeignKey(to='tracking.Clinic')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='clinic',
            field=models.ForeignKey(default=1, to='tracking.Clinic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='treatingprovider',
            name='clinic',
            field=models.ForeignKey(default=1, to='tracking.Clinic'),
            preserve_default=False,
        ),
    ]
