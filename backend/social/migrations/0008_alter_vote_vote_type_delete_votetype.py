# Generated by Django 5.1.2 on 2024-11-06 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0001_squashed_0007_auto_20210902_1733"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="vote_type",
            field=models.CharField(
                choices=[("aye", "Aye"), ("no", "No")], max_length=10
            ),
        ),
        migrations.DeleteModel(
            name="VoteType",
        ),
    ]
