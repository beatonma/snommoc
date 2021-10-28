# Generated by Django 3.0.2 on 2020-03-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0014_auto_20200316_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='parliamentdotuk',
            field=models.PositiveIntegerField(blank=True, help_text='ID used on parliament.uk website', null=True, unique=True),
        ),
        migrations.CreateModel(
            name='PartyAlsoKnownAs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('alias', models.OneToOneField(help_text='An alternative instance, probably with a differently formatted name', on_delete=django.db.models.deletion.CASCADE, related_name='alias', to='repository.Party')),
                ('canonical', models.ForeignKey(help_text='Preferred party instance', on_delete=django.db.models.deletion.CASCADE, related_name='canonical', to='repository.Party')),
            ],
            options={
                'verbose_name': 'PartyAlsoKnownAs',
                'verbose_name_plural': 'Parties also known as',
            },
        ),
    ]