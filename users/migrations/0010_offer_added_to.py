# Generated by Django 3.0.4 on 2020-03-30 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_petition_added_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='added_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Offer'),
        ),
    ]