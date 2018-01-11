# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HealthNet', '0007_auto_20151107_1835'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('notes', models.TextField()),
                ('dosage', models.CharField(max_length=100)),
                ('instructions', models.TextField()),
                ('doctor', models.ForeignKey(related_name='doctor', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(related_name='patient', to='HealthNet.MedicalInformation')),
            ],
        ),
    ]
