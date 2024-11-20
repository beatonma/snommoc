import django.db.models.deletion
import util.models.generics
import util.time
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0059_remove_constituencyboundary_area_and_more"),
    ]

    operations = [
        migrations.DeleteModel("ConstituencyCandidate"),
        migrations.DeleteModel("ConstituencyResultDetail"),
        migrations.CreateModel(
            name="ConstituencyResultDetail",
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
                ("result", models.CharField(max_length=32)),
                ("majority", models.PositiveIntegerField(default=0)),
                ("turnout", models.PositiveIntegerField(default=0)),
                ("electorate", models.PositiveIntegerField(default=0)),
                (
                    "constituency_result",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detail",
                        to="repository.constituencyresult",
                    ),
                ),
            ],
            options={
                "ordering": ["constituency_result"],
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
        migrations.CreateModel(
            name="ConstituencyCandidate",
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
                ("name", models.CharField(max_length=128)),
                ("votes", models.PositiveIntegerField(default=0)),
                ("order", models.PositiveSmallIntegerField(default=100)),
                ("party_name", models.CharField(max_length=128)),
                (
                    "party",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.party",
                    ),
                ),
                (
                    "person",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.person",
                    ),
                ),
                (
                    "election_result",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidates",
                        to="repository.constituencyresultdetail",
                    ),
                ),
            ],
            options={
                "ordering": ["name", "election_result"],
                "unique_together": {("election_result", "name")},
            },
            bases=(models.Model, util.models.generics.BaseModelMixin),
        ),
    ]
