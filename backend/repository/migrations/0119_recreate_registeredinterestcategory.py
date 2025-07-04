# Generated by Django 5.1.3 on 2025-01-16 11:58

import django.db.models.deletion
import util.time
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0118_alter_committeemember_options_and_more"),
    ]

    operations = [
        migrations.DeleteModel(name="RegisteredInterestCategory"),
        migrations.DeleteModel(name="RegisteredInterest"),
        migrations.CreateModel(
            name="RegisteredInterestCategory",
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
                ("created_at", models.DateTimeField(default=util.time.get_now)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("codename_major", models.PositiveSmallIntegerField()),
                (
                    "codename_minor",
                    models.CharField(blank=True, max_length=5, null=True),
                ),
                ("name", models.CharField(max_length=512)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.house",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Registered interest categories",
                "ordering": ("house", "sort_order"),
            },
        ),
        migrations.CreateModel(
            name="RegisteredInterest",
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
                ("created_at", models.DateTimeField(default=util.time.get_now)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website - unique per person"
                    ),
                ),
                ("description", models.TextField()),
                ("created", models.DateField(blank=True, null=True)),
                ("amended", models.DateField(blank=True, null=True)),
                ("deleted", models.DateField(blank=True, null=True)),
                ("is_correction", models.BooleanField(default=False)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="repository.registeredinterest",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="registered_interests",
                        to="repository.person",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.registeredinterestcategory",
                    ),
                ),
            ],
            options={
                "ordering": ("-amended", "-created"),
            },
        ),
        migrations.AddConstraint(
            model_name="registeredinterestcategory",
            constraint=models.UniqueConstraint(
                fields=("codename_major", "codename_minor", "house"),
                name="unique_codename_per_house",
            ),
        ),
        migrations.AddConstraint(
            model_name="registeredinterest",
            constraint=models.UniqueConstraint(
                fields=("parliamentdotuk", "person"), name="unique_id_per_person"
            ),
        ),
    ]
