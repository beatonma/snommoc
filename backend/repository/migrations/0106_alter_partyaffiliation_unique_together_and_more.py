# Generated by Django 5.1.3 on 2024-12-05 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0105_alter_partygenderdemographics_house_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="partyaffiliation",
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name="partyaffiliation",
            constraint=models.UniqueConstraint(
                fields=("start", "person", "party"),
                name="unique_party_per_person_per_startdate",
            ),
        ),
    ]
