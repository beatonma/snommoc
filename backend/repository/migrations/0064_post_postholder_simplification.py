# Generated by Django 5.1.3 on 2024-11-22 11:18

import django.db.models.deletion
import util.time
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0063_rename_post_models"),
    ]

    operations = [
        migrations.DeleteModel(
            name="GovernmentPost",
        ),
        migrations.DeleteModel(
            name="GovernmentPostHolder",
        ),
        migrations.DeleteModel(
            name="OppositionPost",
        ),
        migrations.DeleteModel(
            name="OppositionPostHolder",
        ),
        migrations.DeleteModel(
            name="OtherPost",
        ),
        migrations.DeleteModel(
            name="OtherPostHolder",
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("government", "Government"),
                            ("opposition", "Opposition"),
                            ("other", "Other"),
                        ],
                        max_length=24,
                    ),
                ),
                ("name", models.CharField(max_length=512)),
                (
                    "hansard_name",
                    models.CharField(blank=True, max_length=512, null=True),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="PostHolder",
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
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("start", models.DateField(blank=True, null=True)),
                ("end", models.DateField(blank=True, null=True)),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="posts",
                        to="repository.person",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="holders",
                        to="repository.post",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model,),
        ),
    ]
