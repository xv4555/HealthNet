# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0011_auto_20151107_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='medical_information',
            field=models.ManyToManyField(null=True, to='HealthNet.MedicalInformation', blank=True),
        ),
    ]
