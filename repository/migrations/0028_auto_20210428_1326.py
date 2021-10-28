# Generated by Django 3.2 on 2021-04-28 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0027_auto_20210419_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unlinkedconstituency',
            name='constituency',
        ),
        migrations.AddConstraint(
            model_name='unlinkedconstituency',
            constraint=models.UniqueConstraint(fields=('name', 'mp', 'election'), name='unique_election_result'),
        ),
    ]