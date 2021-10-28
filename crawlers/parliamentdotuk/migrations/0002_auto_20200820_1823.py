# Generated by Django 3.0.7 on 2020-08-20 18:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('parliamentdotuk', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billupdateerror',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commonsdivisionupdateerror',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='electionresultupdateerror',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='lordsdivisionupdateerror',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]