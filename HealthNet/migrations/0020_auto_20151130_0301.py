# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0019_auto_20151130_0300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='patient',
            field=models.ForeignKey(to='HealthNet.UserProfile', null=True),
        ),
    ]
