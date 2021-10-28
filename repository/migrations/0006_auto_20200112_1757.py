# Generated by Django 3.0.2 on 2020-01-12 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20200111_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaredinterest',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='election',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='maidenspeech',
            name='hansard',
            field=models.CharField(blank=True, help_text='Hansard ID', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='maidenspeech',
            name='subject',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]