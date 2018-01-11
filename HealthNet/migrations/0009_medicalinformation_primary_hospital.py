# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0008_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalinformation',
            name='primary_hospital',
            field=models.OneToOneField(blank=True, to='HealthNet.Hospital', null=True),
        ),
    ]
