import json
import re
from dataclasses import asdict, dataclass

from common.models import BaseModel, BaseQuerySet
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, Point


class ConstituencyBoundaryQuerySet(BaseQuerySet):
    def update_geometry(
        self,
        *,
        geojson: str | dict,
        **kwargs,
    ) -> tuple["ConstituencyBoundary", bool]:
        geometry = _boundary_fields(geojson)

        return super().update_or_create(
            **kwargs,
            defaults={
                **asdict(geometry),
                "simple_json": self._build_simple_json(geometry.geometry),
            },
        )

    def resimplify(self, tolerance: float, precision: int):
        for b in self.all():
            b.simple_json = self._build_simple_json(
                b.geometry, tolerance=tolerance, precision=precision
            )
            b.save(update_fields=("simple_json",))

    @staticmethod
    def _build_simple_json(
        geom: GEOSGeometry,
        tolerance: float = 0.001,
        precision: int = 3,
    ) -> str:
        simplified = geom.simplify(tolerance=tolerance)
        serialized = _reduce_decimal_precision(
            simplified.geojson, precision=precision
        ).replace(" ", "")

        return serialized


@dataclass
class BoundaryFields:
    geometry: GEOSGeometry
    north: float
    south: float
    east: float
    west: float
    centroid: Point


def _boundary_fields(geojson_or_geometry: dict | str | GEOSGeometry) -> BoundaryFields:
    if isinstance(geojson_or_geometry, GEOSGeometry):
        geometry = geojson_or_geometry
    else:
        if isinstance(geojson_or_geometry, dict):
            geojson_or_geometry = json.dumps(geojson_or_geometry)
        geometry = GEOSGeometry(_reduce_decimal_precision(geojson_or_geometry, 5))

    [west, south, east, north] = geometry.extent

    return BoundaryFields(
        geometry=geometry,
        north=north,
        south=south,
        east=east,
        west=west,
        centroid=geometry.centroid,
    )


def _reduce_decimal_precision(geojson: str, precision: int) -> str:
    return re.sub(
        r"(?P<integer>\d+)\.(?P<fraction>\d+)",
        lambda match: f"{match.group("integer")}.{match.group("fraction")[:precision]}",
        geojson,
    )


class BaseBoundary(BaseModel):
    class Meta:
        abstract = True

    SRID = 4326

    geometry = models.GeometryField(tolerance=1)

    # Extents of the geometry
    north = models.FloatField()
    south = models.FloatField()
    east = models.FloatField()
    west = models.FloatField()
    centroid = models.PointField()


class ConstituencyBoundary(BaseBoundary):
    objects = ConstituencyBoundaryQuerySet.as_manager()
    constituency = models.OneToOneField(
        "Constituency",
        on_delete=models.CASCADE,
        related_name="boundary",
    )

    # Pre-serialized, simplified approximation of geometry
    simple_json = models.TextField()

    def __str__(self):
        return self.constituency.name

    class Meta:
        verbose_name_plural = "Constituency Boundaries"


class PartyTerritoryQuerySet(BaseQuerySet):
    def generate(self):
        from repository.models import Constituency

        constituencies = Constituency.objects.current().prefetch_related(
            "boundary", "mp__party"
        )
        results: dict[int, GEOSGeometry] = {}

        for constituency in constituencies:
            try:
                party_pk = constituency.mp.party.pk
            except ValueError:
                print(f"could not get party pk {constituency.name}")
                continue

            boundary = constituency.boundary.geometry
            party_boundary = results.get(party_pk, None)

            if party_boundary:
                results[party_pk] = party_boundary.union(boundary)
            else:
                results[party_pk] = boundary

        for party_pk, geometry in results.items():
            self.update_or_create(
                party_id=party_pk,
                defaults=asdict(_boundary_fields(geometry)),
            )


class PartyTerritory(BaseBoundary):
    """The union of ConstituencyBoundary polygons controlled by a party."""

    objects = PartyTerritoryQuerySet.as_manager()
    party = models.OneToOneField(
        "Party",
        on_delete=models.CASCADE,
        related_name="territory",
    )

    def __str__(self):
        return self.party.name
