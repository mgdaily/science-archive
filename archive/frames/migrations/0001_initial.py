# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 23:07
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import pgsphere.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pgsphere', '0001_initial')
    ]

    operations = [
        migrations.CreateModel(
            name='Frame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(db_index=True, max_length=1000, unique=True)),
                ('area', pgsphere.fields.SBoxField()),
                ('DATE_OBS', models.DateTimeField(db_index=True, help_text='Time of observation in UTC. FITS header: DATE-OBS', verbose_name='DATE-OBS')),
                ('USERID', models.CharField(db_index=True, help_text='Textual user id of the frame. FITS header: USERID', max_length=200)),
                ('PROPID', models.CharField(db_index=True, help_text='Textual proposal id. FITS header: PROPID', max_length=200)),
                ('INSTRUME', models.CharField(db_index=True, help_text='Instrument used. FITS header: INSTRUME', max_length=10)),
                ('OBJECT', models.CharField(db_index=True, help_text='Target object name. FITS header: OBJECT', max_length=200)),
                ('SITEID', models.CharField(help_text='Originating site. FITS header: SITEID', max_length=3)),
                ('TELID', models.CharField(help_text='Originating telescope. FITS header: TELID', max_length=4)),
                ('EXPTIME', models.DecimalField(decimal_places=5, help_text='Exposure time, in seconds. FITS header: EXPTIME', max_digits=10)),
                ('FILTER', models.CharField(help_text='Filter used. FITS header: FILTER', max_length=100)),
                ('L1PUBDAT', models.DateTimeField(help_text='The date the frame becomes public. FITS header: L1PUBDAT')),
                ('OBSTYPE', models.CharField(choices=[('BIAS', 'BIAS'), ('DARK', 'DARK'), ('EXPERIMENTAL', 'EXPERIMENTAL'), ('EXPOSE', 'EXPOSE'), ('SKYFLAT', 'SKYFLAT'), ('STANDARD', 'STANDARD')], help_text='Type of observation. FITS header: OBSTYPE', max_length=20)),
                ('related_frames', models.ManyToManyField(blank=True, related_name='_frame_related_frames_+', to='frames.Frame')),
            ],
        ),
        migrations.CreateModel(
            name='Headers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('frame', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='frames.Frame')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=32, unique=True)),
                ('md5', models.CharField(max_length=32, unique=True)),
                ('frame', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frames.Frame')),
            ],
        ),
    ]
