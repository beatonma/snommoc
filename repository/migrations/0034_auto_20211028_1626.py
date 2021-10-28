# Generated by Django 3.2.4 on 2021-10-28 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0033_auto_20210902_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='constituencycandidate',
            old_name='party',
            new_name='party_name',
        ),
        migrations.AddField(
            model_name='constituencycandidate',
            name='person',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.person'),
        ),
        migrations.AlterField(
            model_name='partyalsoknownas',
            name='alias',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='partyalsoknownas',
            name='canonical',
            field=models.ForeignKey(help_text='Preferred party instance', on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to='repository.party'),
        ),
    ]