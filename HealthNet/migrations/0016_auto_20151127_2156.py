# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0015_prescription_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalinformation',
            name='medical_information',
        ),
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(null=True, to='HealthNet.MedicalInformation', related_name='for_patient'),
        ),
    ]
