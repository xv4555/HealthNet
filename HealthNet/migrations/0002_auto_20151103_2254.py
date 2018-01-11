# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospitalstaff',
            name='hospital',
        ),
        migrations.RemoveField(
            model_name='hospitalstaff',
            name='user_profile',
        ),
        migrations.DeleteModel(
            name='HospitalStaff',
        ),
    ]
