# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0002_auto_20151103_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalStaff',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('hospital', models.ForeignKey(to='HealthNet.Hospital')),
                ('user_profile', models.ForeignKey(to='HealthNet.UserProfile')),
            ],
        ),
    ]
