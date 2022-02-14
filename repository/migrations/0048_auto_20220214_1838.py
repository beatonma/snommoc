# Generated by Django 3.2.4 on 2022-02-14 18:38

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models

import util.models.generics
import util.time


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0047_auto_20211207_1418"),
    ]

    operations = [
        migrations.CreateModel(
            name="BillAgent",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=256)),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("website", models.URLField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="BillStage",
            fields=[
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "abbreviation",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                ("sort_order", models.PositiveSmallIntegerField()),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="BillTypeCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=32, unique=True)),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="Organisation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=512)),
                ("url", models.URLField(blank=True, null=True)),
            ],
            options={
                "ordering": ["name"],
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AddField(
            model_name="bill",
            name="bill_withdrawn",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bill",
            name="current_house",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bills_current",
                to="repository.house",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="included_sessions",
            field=models.ManyToManyField(
                related_name="bills", to="repository.ParliamentarySession"
            ),
        ),
        migrations.AddField(
            model_name="bill",
            name="introduced_session",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bills_introduced",
                to="repository.parliamentarysession",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="is_act",
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="is_defeated",
            field=models.BooleanField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="last_update",
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="long_title",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bill",
            name="originating_house",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bills_originated",
                to="repository.house",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="petitioning_information",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bill",
            name="petitioning_period",
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name="bill",
            name="short_title",
            field=models.CharField(default=None, max_length=512),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="summary",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="parliamentarysession",
            name="name",
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.CreateModel(
            name="BillType",
            fields=[
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("description", models.TextField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="repository.billtypecategory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="BillStageType",
            fields=[
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                (
                    "house",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.house",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="BillStageSitting",
            fields=[
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                (
                    "parliamentdotuk",
                    models.PositiveIntegerField(
                        help_text="ID used on parliament.uk website",
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("date", models.DateTimeField()),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sittings",
                        to="repository.billstage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AddField(
            model_name="billstage",
            name="bill",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="repository.bill"
            ),
        ),
        migrations.AddField(
            model_name="billstage",
            name="session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bill_stages",
                to="repository.parliamentarysession",
            ),
        ),
        migrations.AddField(
            model_name="billstage",
            name="stage_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="repository.billstagetype",
            ),
        ),
        migrations.CreateModel(
            name="BillSponsor",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateTimeField(default=util.time.get_now)),
                ("modified_on", models.DateTimeField(auto_now=True)),
                ("sort_order", models.PositiveSmallIntegerField()),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sponsors",
                        to="repository.bill",
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sponsored_bills",
                        to="repository.person",
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sponsored_bills",
                        to="repository.organisation",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.AddField(
            model_name="bill",
            name="agent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="repository.billagent",
            ),
        ),
        migrations.AddField(
            model_name="bill",
            name="bill_type",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="repository.billtype",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="bill",
            name="current_stage",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="+",
                to="repository.billstage",
            ),
        ),
        migrations.AddField(
            model_name="bill",
            name="promoters",
            field=models.ManyToManyField(
                related_name="promoted_bills", to="repository.Organisation"
            ),
        ),
    ]
