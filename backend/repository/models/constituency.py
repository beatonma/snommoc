from django.db import models
from repository.models.mixins import (
    BaseModel,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
    SocialMixin,
)


class Constituency(SocialMixin, ParliamentDotUkMixin, PeriodMixin, BaseModel):
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Current representative",
    )

    ordinance_survey_name = models.CharField(max_length=64, null=True, blank=True)
    gss_code = models.CharField(
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        help_text="Government Statistical Service ID",
    )

    def social_title(self) -> str:
        return self.name

    def __str__(self):
        return f"{self.name} [{self.parliamentdotuk}] {self.describe_timespan()}"

    class Meta:
        verbose_name_plural = "Constituencies"


class ConstituencyBoundary(BaseModel):
    constituency = models.OneToOneField(
        "Constituency",
        on_delete=models.CASCADE,
    )
    geo_json = models.JSONField()

    def __str__(self):
        return self.constituency.name

    class Meta:
        verbose_name_plural = "Constituency Boundaries"


class ConstituencyRepresentative(PersonMixin, PeriodMixin, BaseModel):
    person = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        related_name="constituencies",
    )
    constituency = models.ForeignKey(
        "Constituency",
        on_delete=models.CASCADE,
        related_name="representatives",
        related_query_name="representative",
    )

    def election_results(self):
        from repository.models import ConstituencyResult

        return ConstituencyResult.objects.filter_date_range(
            self.start, self.end
        ).filter(
            person=self.person,
            constituency=self.constituency,
        )

    def __str__(self):
        return f"{self.constituency.name} {self.describe_timespan()}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "constituency", "start"],
                name="unique_person_per_constituency_per_startdate",
            ),
        ]
