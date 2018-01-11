# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0017_auto_20151127_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(null=True, to='HealthNet.MedicalInformation'),
        ),
    ]
