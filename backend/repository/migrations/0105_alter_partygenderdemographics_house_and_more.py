# Generated by Django 5.1.3 on 2024-12-03 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "repository",
            "0104_rename_partydemographics_partygenderdemographics_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="partygenderdemographics",
            name="house",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gender_demographics",
                to="repository.house",
            ),
        ),
        migrations.AlterField(
            model_name="partygenderdemographics",
            name="party",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gender_demographics",
                to="repository.party",
            ),
        ),
    ]
