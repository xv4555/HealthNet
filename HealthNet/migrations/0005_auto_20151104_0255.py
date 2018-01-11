# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0004_transfers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfers',
            name='receiver',
            field=models.ForeignKey(null=True, blank=True, to='HealthNet.UserProfile', related_name='receiver'),
        ),
    ]
