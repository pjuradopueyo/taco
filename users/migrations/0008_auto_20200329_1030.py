# Generated by Django 3.0.4 on 2020-03-29 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200329_1012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petition',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='petition',
            name='longitude',
        ),
        migrations.AddField(
            model_name='place',
            name='place_main_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
