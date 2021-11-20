# Generated by Django 3.2.4 on 2021-11-18 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0039_alter_billsponsor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billpublication',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', related_query_name='publication', to='repository.bill'),
        ),
        migrations.AlterField(
            model_name='billsponsor',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', related_query_name='sponsor', to='repository.bill'),
        ),
        migrations.AlterField(
            model_name='billsponsor',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsored_bills', related_query_name='sponsored_bill', to='repository.person'),
        ),
        migrations.AlterField(
            model_name='billstage',
            name='bill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='repository.bill'),
        ),
    ]