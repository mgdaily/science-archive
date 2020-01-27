# Generated by Django 2.0.13 on 2020-01-23 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frames', '0010_version_migrated'),
    ]

    operations = [
        migrations.AddField(
            model_name='frame',
            name='DAY_OBS',
            field=models.DateField(help_text='Observing Night in YYYYMMDD. FITS header: DAY-OBS', null=True, verbose_name='DAY-OBS'),
        ),
    ]