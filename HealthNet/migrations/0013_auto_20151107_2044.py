# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0012_prescription_medical_information'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='medical_information',
        ),
        migrations.AddField(
            model_name='prescription',
            name='medical_information',
            field=models.ForeignKey(null=True, blank=True, to='HealthNet.MedicalInformation'),
        ),
    ]
