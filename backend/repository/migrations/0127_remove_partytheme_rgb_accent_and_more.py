# Generated by Django 5.1.6 on 2025-02-17 16:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0126_alter_constituencyboundary_geometry_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="partytheme",
            name="rgb_accent",
        ),
        migrations.RemoveField(
            model_name="partytheme",
            name="rgb_on_accent",
        ),
        migrations.RemoveField(
            model_name="partytheme",
            name="rgb_on_primary",
        ),
        migrations.RemoveField(
            model_name="partytheme",
            name="rgb_primary",
        ),
    ]
