# Generated by Django 3.0.2 on 2020-04-07 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0018_person_current_post'),
        ('surface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedLordsDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.LordsDivision')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeaturedCommonsDivision',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.CommonsDivision')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
