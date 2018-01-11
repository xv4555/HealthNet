# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0014_auto_20151107_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(to='HealthNet.UserProfile', related_name='for_patient', null=True),
        ),
    ]
