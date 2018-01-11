# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateTimeField()),
                ('doctor', models.ForeignKey(related_name='doctor_appointments', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(related_name='patient_appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=30)),
                ('relationship', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('hospital_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
                ('zipcode', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='HospitalStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('hospital', models.ForeignKey(to='HealthNet.Hospital')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalStay',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('admission', models.DateTimeField(auto_now_add=True)),
                ('discharge', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('policy_number', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalInformation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('sex', models.CharField(max_length=50)),
                ('medications', models.CharField(null=True, max_length=400)),
                ('allergies', models.CharField(null=True, max_length=400)),
                ('medical_conditions', models.CharField(null=True, max_length=400)),
                ('family_history', models.CharField(null=True, max_length=400)),
                ('additional_info', models.CharField(null=True, max_length=600)),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('read', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('phone_number', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserStatus',
            fields=[
                ('status_id', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.ForeignKey(null=True, to='HealthNet.UserStatus'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='user_from',
            field=models.ForeignKey(to='HealthNet.UserProfile', null=True, related_name='user_from'),
        ),
        migrations.AddField(
            model_name='message',
            name='user_to',
            field=models.ForeignKey(related_name='user_to', to='HealthNet.UserProfile'),
        ),
        migrations.AddField(
            model_name='medicalinformation',
            name='user',
            field=models.OneToOneField(to='HealthNet.UserProfile', null=True),
        ),
        migrations.AddField(
            model_name='insurance',
            name='medical_information',
            field=models.ForeignKey(null=True, to='HealthNet.MedicalInformation'),
        ),
        migrations.AddField(
            model_name='hospitalstay',
            name='doctor',
            field=models.ForeignKey(to='HealthNet.UserProfile', null=True, related_name='referring_doctor'),
        ),
        migrations.AddField(
            model_name='hospitalstay',
            name='hospital',
            field=models.ForeignKey(to='HealthNet.Hospital'),
        ),
        migrations.AddField(
            model_name='hospitalstay',
            name='nurse',
            field=models.ForeignKey(to='HealthNet.UserProfile', null=True, related_name='referring_nurse'),
        ),
        migrations.AddField(
            model_name='hospitalstay',
            name='patient',
            field=models.ForeignKey(related_name='patient', to='HealthNet.UserProfile'),
        ),
        migrations.AddField(
            model_name='hospitalstaff',
            name='user_profile',
            field=models.ForeignKey(to='HealthNet.UserProfile'),
        ),
        migrations.AddField(
            model_name='emergencycontact',
            name='user_profile_id',
            field=models.ForeignKey(null=True, to='HealthNet.MedicalInformation'),
        ),
    ]
