import json
import re
from typing import Self

from common.models import BaseModel, BaseQuerySet
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Q
from repository.models.mixins import (
    AsciiNameMixin,
    ParliamentDotUkMixin,
    PeriodMixin,
    PersonMixin,
    SocialMixin,
)


class ConstituencyQuerySet(BaseQuerySet):
    def search(self, query: str) -> Self:
        query = query.strip()
        return self.filter(
            Q(name__icontains=query)
            | Q(ascii_name__icontains=query)
            | Q(mp__name__icontains=query)
        )

    def current(self) -> Self:
        return self.filter(start__isnull=False, end__isnull=True)

    def historic(self) -> Self:
        return self.filter(end__isnull=False)


class Constituency(
    SocialMixin,
    ParliamentDotUkMixin,
    PeriodMixin,
    AsciiNameMixin,
    BaseModel,
):
    objects = ConstituencyQuerySet.as_manager()
    name = models.CharField(max_length=64)
    mp = models.OneToOneField(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Current representative",
        related_name="constituency",
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

    def save(self, *args, **kwargs):
        self.update_ascii_name(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.parliamentdotuk}] {self.describe_timespan()}"

    class Meta:
        verbose_name_plural = "Constituencies"


class BoundaryQuerySet(BaseQuerySet):
    def update(
        self,
        *,
        geojson: str | dict,
        **kwargs,
    ) -> tuple["ConstituencyBoundary", bool]:
        if isinstance(geojson, dict):
            geojson = json.dumps(geojson)

        geometry = GEOSGeometry(self._reduce_decimal_precision(geojson, 5))
        [west, south, east, north] = geometry.extent

        return super().update_or_create(
            **kwargs,
            defaults={
                "geometry": geometry,
                "simple_json": self._build_simple_json(geometry),
                "north": north,
                "south": south,
                "east": east,
                "west": west,
                "centroid": geometry.centroid,
            },
        )

    @staticmethod
    def _reduce_decimal_precision(geojson: str, precision: int) -> str:
        return re.sub(
            r"(?P<integer>\d+)\.(?P<fraction>\d+)",
            lambda match: f"{match.group("integer")}.{match.group("fraction")[:precision]}",
            geojson,
        )

    def _build_simple_json(self, geom: GEOSGeometry, tolerance: float = 0.01) -> str:
        simplified = geom.simplify(tolerance=tolerance)
        serialized = self._reduce_decimal_precision(
            simplified.geojson, precision=2
        ).replace(" ", "")

        return serialized


class ConstituencyBoundary(BaseModel):
    objects = BoundaryQuerySet.as_manager()
    constituency = models.OneToOneField(
        "Constituency",
        on_delete=models.CASCADE,
        related_name="boundary",
    )
    geometry = models.MultiPolygonField(tolerance=1)

    # Extents of the geometry
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()
    centroid = models.PointField()

    # Pre-serialized, simplified approximation of geometry
    simple_json = models.TextField()

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
        ordering = PeriodMixin.meta_ordering_recent()
