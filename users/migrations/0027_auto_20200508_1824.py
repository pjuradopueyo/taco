# Generated by Django 3.0.4 on 2020-05-08 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_petition_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagpetition',
            name='petition',
        ),
        migrations.RemoveField(
            model_name='tagpetition',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='tagprovider',
            name='provider',
        ),
        migrations.RemoveField(
            model_name='tagprovider',
            name='tag',
        ),
        migrations.DeleteModel(
            name='TagOffer',
        ),
        migrations.DeleteModel(
            name='TagPetition',
        ),
        migrations.DeleteModel(
            name='TagProvider',
        ),
    ]
