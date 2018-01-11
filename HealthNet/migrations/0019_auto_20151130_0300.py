# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0018_auto_20151130_0227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalinformation',
            name='primary_hospital',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='primary_hospital',
            field=models.ForeignKey(null=True, to='HealthNet.Hospital', blank=True),
        ),
    ]
