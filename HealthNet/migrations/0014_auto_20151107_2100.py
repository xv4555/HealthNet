# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0013_auto_20151107_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medical_information',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='patient',
        ),
        migrations.AddField(
            model_name='medicalinformation',
            name='medical_information',
            field=models.ForeignKey(null=True, to='HealthNet.Prescription', blank=True),
        ),
    ]
