# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0006_auto_20151107_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transfers',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='transfers',
            name='status',
        ),
    ]
