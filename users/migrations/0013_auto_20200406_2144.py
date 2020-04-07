# Generated by Django 3.0.4 on 2020-04-06 21:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200402_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='answer_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_to_petition', to='users.Petition'),
        ),
        migrations.AddField(
            model_name='petition',
            name='petition_type',
            field=models.CharField(default='petition', max_length=10),
        ),
        migrations.AddField(
            model_name='petition',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Provider'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='added_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_to_petition', to='users.Petition'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='intensity',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='petition',
            name='start_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
    ]