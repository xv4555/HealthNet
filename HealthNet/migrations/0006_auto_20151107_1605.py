# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0005_auto_20151104_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='notes',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='medicalinformation',
            name='height',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='medicalinformation',
            name='weight',
            field=models.CharField(max_length=5),
        ),
    ]
