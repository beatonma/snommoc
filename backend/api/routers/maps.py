from api.pagination import offset_pagination
from api.schema.maps import ConstituencyMapSchema, PartyMapSchema
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpRequest
from ninja import Query, Router, Schema
from ninja.pagination import paginate
from repository.models import Constituency, Party
from repository.models.geography.boundaries import BaseBoundary

router = Router(tags=["Maps"])


class MapQuery(Schema):
    # If provided, results will be sorted by closeness to the locus.
    locus_latitude: float = None
    locus_longitude: float = None


@router.get("/constituencies/", response=list[ConstituencyMapSchema])
@paginate(offset_pagination(50))
def constituencies(request: HttpRequest, query: Query[MapQuery]):
    qs = Constituency.objects.current().prefetch_related(
        "boundary", "mp", "mp__party", "mp__party__theme"
    )

    if query.locus_longitude and query.locus_latitude:
        from django.contrib.gis.geos import Point

        point = Point(
            query.locus_longitude, query.locus_latitude, srid=BaseBoundary.SRID
        )
        return qs.annotate(distance=Distance("boundary__geometry", point)).order_by(
            "distance"
        )

    return qs.order_by("-boundary__north")


@router.get("/parties/", response=list[PartyMapSchema])
def parties(request: HttpRequest):
    return (
        Party.objects.current()
        .prefetch_related("territory")
        .order_by("-territory__north")
    )
