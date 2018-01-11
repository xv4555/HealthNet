# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0009_medicalinformation_primary_hospital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalinformation',
            name='primary_hospital',
            field=models.ForeignKey(to='HealthNet.Hospital', blank=True, null=True),
        ),
    ]
