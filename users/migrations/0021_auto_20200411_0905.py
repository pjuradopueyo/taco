# Generated by Django 3.0.4 on 2020-04-11 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_petition_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='slug',
            field=models.CharField(default='churrito', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='petition',
            name='added_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_to_petition', to='users.Petition'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='answer_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_to_petition', to='users.Petition'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Place'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Product'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Provider'),
        ),
        migrations.AlterField(
            model_name='petition',
            name='radio',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='petition',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='place',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Country'),
        ),
        migrations.AlterField(
            model_name='place',
            name='door_name',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='floor_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='google_place',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='postal',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='street',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='street_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='place',
            name='town',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
