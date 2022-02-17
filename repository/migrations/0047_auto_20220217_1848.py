# Generated by Django 3.2.4 on 2022-02-17 18:48

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models

import util.models.generics
import util.time


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0046_delete_bill_20211207_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('long_title', models.TextField(blank=True, null=True)),
                ('summary', models.TextField(blank=True, help_text='HTML-formatted description', null=True)),
                ('last_update', models.DateTimeField()),
                ('withdrawn_at', models.DateTimeField(blank=True, null=True)),
                ('is_defeated', models.BooleanField()),
                ('is_act', models.BooleanField()),
                ('petitioning_period', models.CharField(blank=True, max_length=512, null=True)),
                ('petitioning_information', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillAgent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillPublication',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('display_date', models.DateTimeField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publications', to='repository.bill')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.house')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillPublicationType',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillStage',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('abbreviation', models.CharField(blank=True, max_length=16, null=True)),
                ('sort_order', models.PositiveSmallIntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='repository.bill')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.house')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillTypeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AlterField(
            model_name='parliamentarysession',
            name='name',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.CreateModel(
            name='BillType',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.billtypecategory')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillStageType',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.house')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillStageSitting',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField()),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sittings', to='repository.billstage')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AddField(
            model_name='billstage',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bill_stages', to='repository.parliamentarysession'),
        ),
        migrations.AddField(
            model_name='billstage',
            name='stage_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.billstagetype'),
        ),
        migrations.CreateModel(
            name='BillSponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('sort_order', models.PositiveSmallIntegerField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsors', to='repository.bill')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsored_bills', to='repository.person')),
                ('organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsored_bills', to='repository.organisation')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name='BillPublicationLink',
            fields=[
                ('created_on', models.DateTimeField(default=util.time.get_now)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('parliamentdotuk', models.PositiveIntegerField(help_text='ID used on parliament.uk website', primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('content_type', models.CharField(max_length=64)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='repository.billpublication')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AddField(
            model_name='billpublication',
            name='publication_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.billpublicationtype'),
        ),
        migrations.AddField(
            model_name='bill',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.billagent'),
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.billtype'),
        ),
        migrations.AddField(
            model_name='bill',
            name='current_house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills_current', to='repository.house'),
        ),
        migrations.AddField(
            model_name='bill',
            name='current_stage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='repository.billstage'),
        ),
        migrations.AddField(
            model_name='bill',
            name='originating_house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills_originated', to='repository.house'),
        ),
        migrations.AddField(
            model_name='bill',
            name='promoters',
            field=models.ManyToManyField(related_name='promoted_bills', to='repository.Organisation'),
        ),
        migrations.AddField(
            model_name='bill',
            name='session_introduced',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills_introduced', to='repository.parliamentarysession'),
        ),
        migrations.AddField(
            model_name='bill',
            name='sessions',
            field=models.ManyToManyField(related_name='bills', to='repository.ParliamentarySession'),
        ),
    ]
