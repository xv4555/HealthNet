# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0016_auto_20151127_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(to='HealthNet.MedicalInformation', null=True, to_field='user'),
        ),
    ]
