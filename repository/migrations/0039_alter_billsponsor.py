# Generated by Django 3.2.4 on 2021-11-18 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0038_auto_20211104_1644"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="billsponsor",
            options={"ordering": ["name"]},
        ),
        migrations.AlterUniqueTogether(
            name="billsponsor",
            unique_together={("person", "bill"), ("name", "bill")},
        ),
    ]
