# Generated by Django 5.1.3 on 2024-11-24 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "repository",
            "0087_remove_registeredinterest_unique_id_per_category_and_more",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="experience",
            name="unique_title_per_person_per_startdate",
        ),
    ]
