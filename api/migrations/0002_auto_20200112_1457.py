# Generated by Django 3.0.2 on 2020-01-12 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apikey',
            options={'permissions': (('read_snommoc_api', 'Can read data from the snommoc API.'),)},
        ),
    ]
