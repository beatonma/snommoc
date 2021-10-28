# Generated by Django 3.0.2 on 2020-05-11 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0022_auto_20200511_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.House'),
        ),
        migrations.CreateModel(
            name='ConstituencyResultDetail',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('electorate', models.PositiveIntegerField(default=0)),
                ('majority', models.PositiveIntegerField(default=0)),
                ('turnout', models.PositiveIntegerField(default=0)),
                ('turnout_fraction', models.DecimalField(decimal_places=3, max_digits=3)),
                ('result', models.CharField(max_length=32)),
                ('constituency_result', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='result_detail', to='repository.ConstituencyResult')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='constituencycandidate',
            name='election_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='repository.ConstituencyResultDetail'),
        ),
        migrations.DeleteModel(
            name='ElectionResult',
        ),
    ]
