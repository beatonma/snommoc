# Generated by Django 3.2 on 2021-09-02 17:33

from django.db import migrations, models
import util.time


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0008_tasknotification_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasknotification',
            name='created_on',
            field=models.DateTimeField(default=util.time.get_now),
        ),
    ]
