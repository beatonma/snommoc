# Generated by Django 2.2.6 on 2019-11-09 22:03

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('ordinance_survey_name', models.CharField(blank=True, max_length=64, null=True)),
                ('gss_code', models.CharField(blank=True, help_text='Government Statistical Service ID', max_length=12, null=True)),
                ('constituency_type', models.CharField(choices=[('county', 'County'), ('borough', 'Borough')], default='county', help_text='Borough, county...', max_length=10, null=True)),
            ],
            options={
                'verbose_name_plural': 'Constituencies',
            },
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wikipedia', models.CharField(blank=True, help_text="Path section of a wikipedia url (e.g. 'John_Baron_(politician)')", max_length=64, null=True)),
                ('phone_parliament', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='National office phone number', max_length=128, null=True, region=None)),
                ('phone_constituency', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Local office phone number', max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
            options={
                'verbose_name_plural': 'Personal links',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wikipedia', models.CharField(blank=True, help_text="Path section of a wikipedia url (e.g. 'John_Baron_(politician)')", max_length=64, null=True)),
                ('name', models.CharField(max_length=32, unique=True)),
                ('short_name', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('long_name', models.CharField(blank=True, help_text='Official name', max_length=64, null=True, unique=True)),
                ('homepage', models.URLField(blank=True, null=True)),
                ('year_founded', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Canonical name for this person.', max_length=72)),
                ('given_name', models.CharField(help_text='First name', max_length=72, null=True)),
                ('family_name', models.CharField(help_text='Last name', max_length=72, null=True)),
                ('additional_name', models.CharField(blank=True, help_text='Middle name(s)', max_length=72, null=True)),
                ('gender', models.CharField(blank=True, default=None, max_length=16, null=True)),
            ],
            options={
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='WebLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('links', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weblinks', related_query_name='weblink', to='repository.Links')),
            ],
        ),
        migrations.CreateModel(
            name='Mp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', null=True, unique=True)),
                ('theyworkforyou', models.PositiveIntegerField(help_text='ID used on theyworkforyou.com', null=True, unique=True)),
                ('party', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parties', related_query_name='party', to='repository.Party')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', related_query_name='person', to='repository.Person')),
            ],
            options={
                'verbose_name': 'MP',
                'verbose_name_plural': 'MPs',
            },
        ),
        migrations.AddField(
            model_name='links',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='links', related_query_name='links', to='repository.Person'),
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=48)),
                ('category', models.CharField(choices=[('political', 'political'), ('country', 'country')], default='political', max_length=16)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interests', related_query_name='interest', to='repository.Person')),
            ],
        ),
        migrations.CreateModel(
            name='ConstituencyBoundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boundary', models.TextField(help_text='KML file content')),
                ('constituency', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Constituency')),
            ],
        ),
        migrations.AddField(
            model_name='constituency',
            name='mp',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='constituency', to='repository.Mp'),
        ),
    ]