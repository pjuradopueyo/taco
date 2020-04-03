# Generated by Django 3.0.4 on 2020-04-02 22:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_offer_added_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applause',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('claps', models.IntegerField()),
                ('progress', models.IntegerField(blank=True, null=True)),
                ('petition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Petition')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
