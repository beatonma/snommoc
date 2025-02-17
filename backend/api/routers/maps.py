from api.pagination import offset_pagination
from api.schema.maps import ConstituencyMapSchema, PartyMapSchema
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Query, Router, Schema
from ninja.pagination import paginate
from repository.models import Constituency, Party
from repository.models.geography.boundaries import BaseBoundary

router = Router(tags=["Maps"])


class MapQuery(Schema):
    latitude: float = None
    longitude: float = None


@router.get("/constituencies/", response=list[ConstituencyMapSchema])
@paginate(offset_pagination(50))
def constituencies(request: HttpRequest, query: Query[MapQuery]):
    qs = Constituency.objects.current().prefetch_related(
        "boundary", "mp", "mp__party", "mp__party__theme"
    )

    return _order_by_distance_to(
        qs,
        geometry_field="boundary__geometry",
        query=query,
        default_order_by="-boundary__north",
    )


@router.get("/parties/", response=list[PartyMapSchema])
def parties(request: HttpRequest, query: Query[MapQuery]):
    qs = Party.objects.current().prefetch_related("territory")

    return _order_by_distance_to(
        qs,
        geometry_field="territory__geometry",
        query=query,
        default_order_by="-territory__north",
    )


def _order_by_distance_to(
    qs: QuerySet, *, geometry_field: str, query: Query[MapQuery], default_order_by: str
):
    if query.latitude is not None and query.longitude is not None:
        point = Point(x=query.longitude, y=query.latitude, srid=BaseBoundary.SRID)
        return qs.annotate(distance=Distance(geometry_field, point)).order_by(
            "distance"
        )

    return qs.order_by(default_order_by)
