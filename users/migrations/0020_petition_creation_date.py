# Generated by Django 3.0.4 on 2020-04-09 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200409_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='creation_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]
