# Generated by Django 3.2.4 on 2022-03-04 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0049_billsponsor_unique_billsponsor_per_bill'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billstagesitting',
            options={'ordering': ['-date']},
        ),
    ]
