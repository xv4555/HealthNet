# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0003_hospitalstaff'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('date_accepted', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField()),
                ('from_hospital', models.ForeignKey(related_name='from_hospital', to='HealthNet.Hospital')),
                ('receiver', models.ForeignKey(related_name='receiver', to='HealthNet.UserProfile')),
                ('sender', models.ForeignKey(related_name='sender', to='HealthNet.UserProfile')),
                ('to_hospital', models.ForeignKey(related_name='to_hospital', to='HealthNet.Hospital')),
                ('transfer_patient', models.ForeignKey(related_name='transfer_patient', to='HealthNet.UserProfile')),
            ],
        ),
    ]
