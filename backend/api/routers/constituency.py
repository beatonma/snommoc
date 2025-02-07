from api.pagination import offset_pagination
from api.schema.constituency import ConstituencyFullSchema, NationalMapSchema
from api.schema.includes import ConstituencyMiniSchema
from api.schema.types import ParliamentId
from django.db.models import F
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Constituency

router = Router(tags=["Constituencies"])


@router.get(
    "/",
    response=list[ConstituencyMiniSchema],
    description="Searchable constituencies. If no query, returns current constituencies.",
)
@paginate
def constituencies(request: HttpRequest, query: str = None):
    qs = Constituency.objects.all()

    if query:
        qs = qs.search(query)
    else:
        qs = qs.current()

    return qs.order_by(F("end").desc(nulls_first=True), "name")


@router.get("/maps/", response=list[NationalMapSchema])
@paginate(offset_pagination(50))
def maps(request: HttpRequest):
    return (
        Constituency.objects.current()
        .prefetch_related("boundary", "mp", "mp__party", "mp__party__theme")
        .order_by("-boundary__north")
    )


@router.get("/{parliamentdotuk}/", response=ConstituencyFullSchema)
def constituency(request: HttpRequest, parliamentdotuk: ParliamentId):
    return get_object_or_404(Constituency, parliamentdotuk=parliamentdotuk)
