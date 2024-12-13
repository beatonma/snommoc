from api.schema.constituency import ConstituencyFullSchema, ConstituencyResultSchema
from api.schema.includes import ConstituencyMiniSchema
from api.schema.types import ParliamentId
from django.db.models import F
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Constituency, ConstituencyResultDetail

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


@router.get("/{parliamentdotuk}/", response=ConstituencyFullSchema)
def constituency(request: HttpRequest, parliamentdotuk: ParliamentId):
    return get_object_or_404(Constituency, parliamentdotuk=parliamentdotuk)


@router.get(
    "/{constituency_parliamentdotuk}/election/{election_parliamentdotuk}/",
    response=ConstituencyResultSchema,
)
def constituency_election_result(
    request: HttpRequest,
    constituency_parliamentdotuk: ParliamentId,
    election_parliamentdotuk: ParliamentId,
):
    return get_object_or_404(
        ConstituencyResultDetail,
        constituency_result__constituency__parliamentdotuk=constituency_parliamentdotuk,
        constituency_result__election__parliamentdotuk=election_parliamentdotuk,
    )
