# Generated by Django 3.0.2 on 2020-04-14 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0002_signinserviceprovider_usertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='provider_account_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]