# Generated by Django 5.1.3 on 2024-11-12 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0052_remove_commonsdivisionvote_abstention_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="partytheme",
            name="accent_color",
            field=models.CharField(help_text="Hex color code", max_length=10),
        ),
        migrations.AlterField(
            model_name="partytheme",
            name="accent_text_color",
            field=models.CharField(
                choices=[("#ffffff", "light"), ("#000000", "dark")],
                help_text="Color for text that overlays accent",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="partytheme",
            name="party",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="theme",
                to="repository.party",
            ),
        ),
        migrations.AlterField(
            model_name="partytheme",
            name="primary_color",
            field=models.CharField(help_text="Hex color code", max_length=10),
        ),
        migrations.AlterField(
            model_name="partytheme",
            name="primary_text_color",
            field=models.CharField(
                choices=[("#ffffff", "light"), ("#000000", "dark")],
                help_text="Color for text that overlays primary",
                max_length=10,
            ),
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="primary_color",
            new_name="primary",
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="accent_color",
            new_name="accent",
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="primary_text_color",
            new_name="on_primary",
        ),
        migrations.RenameField(
            model_name="partytheme",
            old_name="accent_text_color",
            new_name="on_accent",
        ),
    ]
