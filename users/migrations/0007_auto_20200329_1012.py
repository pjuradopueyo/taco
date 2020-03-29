# Generated by Django 3.0.4 on 2020-03-29 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200329_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatar/'),
        ),
        migrations.AddField(
            model_name='offer',
            name='offer_img',
            field=models.ImageField(blank=True, null=True, upload_to='offer/'),
        ),
        migrations.AddField(
            model_name='petition',
            name='petition_img',
            field=models.ImageField(blank=True, null=True, upload_to='petition/'),
        ),
        migrations.AddField(
            model_name='provider',
            name='secondary_image_1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='provider',
            name='secondary_image_2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='provider',
            name='secondary_image_3',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='provider',
            name='secondary_image_4',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.CreateModel(
            name='TagProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Provider')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(max_length=500)),
                ('coupon_main_img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('price', models.IntegerField()),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Provider')),
            ],
        ),
    ]
