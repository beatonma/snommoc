# Generated by Django 3.0.2 on 2020-03-21 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20200112_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasknotification',
            name='parent',
        ),
    ]
