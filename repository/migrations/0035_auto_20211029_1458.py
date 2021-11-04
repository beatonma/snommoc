# Generated by Django 3.2.4 on 2021-10-29 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0034_auto_20211028_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='constituencycandidate',
            name='party',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.party'),
        ),
        migrations.AlterField(
            model_name='partyalsoknownas',
            name='canonical',
            field=models.ForeignKey(blank=True, help_text='Preferred party instance', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='repository.party'),
        ),
    ]