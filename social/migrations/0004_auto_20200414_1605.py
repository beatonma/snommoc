# Generated by Django 3.0.2 on 2020-04-14 16:05

from django.db import migrations, models
import social.models.token


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_auto_20200414_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='username',
            field=models.CharField(default=social.models.token._create_default_username, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='provider_account_id',
            field=models.CharField(editable=False, max_length=100, unique=True),
        ),
    ]