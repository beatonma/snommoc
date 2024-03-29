# Generated by Django 3.0.7 on 2021-04-19 13:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_remove_tasknotification_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasknotification',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
