# Generated by Django 5.1.3 on 2024-11-23 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0076_alter_housemembership_person"),
    ]

    operations = [
        migrations.AlterField(
            model_name="constituencyrepresentative",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="constituencies",
                to="repository.person",
            ),
        ),
    ]
