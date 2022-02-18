# Generated by Django 3.0.2 on 2020-04-07 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0001_squashed_0033_auto_20210902_1733"),
        ("surface", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeaturedLordsDivision",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("start", models.DateField(blank=True, null=True)),
                ("end", models.DateField(blank=True, null=True)),
                (
                    "division",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="repository.LordsDivision",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FeaturedCommonsDivision",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("start", models.DateField(blank=True, null=True)),
                ("end", models.DateField(blank=True, null=True)),
                (
                    "division",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="repository.CommonsDivision",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
