# Generated by Django 4.2.1 on 2023-06-04 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_alter_event_end_time_alter_event_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2023, 6, 4, 7, 34, 44, 662299, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=datetime.datetime(2023, 6, 4, 7, 34, 44, 662282, tzinfo=datetime.timezone.utc)),
        ),
    ]
