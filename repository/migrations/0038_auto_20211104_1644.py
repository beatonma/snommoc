# Generated by Django 3.2.4 on 2021-11-04 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0037_alter_partyalsoknownas_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constituencycandidate',
            options={'ordering': ['name', 'election_result']},
        ),
        migrations.AlterModelOptions(
            name='constituencyresult',
            options={'ordering': ['constituency', 'election']},
        ),
        migrations.AlterModelOptions(
            name='constituencyresultdetail',
            options={'ordering': ['constituency_result']},
        ),
    ]