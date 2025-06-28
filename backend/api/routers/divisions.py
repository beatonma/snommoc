from api.cache import cache_crawled_data_view
from api.schema.division import (
    CommonsDivisionSchema,
    LordsDivisionSchema,
    VoteWithPersonSchema,
)
from api.schema.includes import DivisionMiniSchema
from api.schema.types import DivisionVoteType
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import CommonsDivision, DivisionVote, LordsDivision
from repository.models.divisions import Division

router = Router(tags=["Divisions"])


@router.get("/", response=list[DivisionMiniSchema])
@paginate
@cache_crawled_data_view
def divisions(request: HttpRequest, query: str = None):
    qs = Division.objects.all()

    if query:
        qs = qs.search(query)

    return qs


@router.get("/commons/", response=list[DivisionMiniSchema])
@paginate
def commons_divisions(request: HttpRequest):
    return CommonsDivision.objects.all()


@router.get("/commons/{parliamentdotuk}/", response=CommonsDivisionSchema)
def commons_division(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(CommonsDivision, parliamentdotuk=parliamentdotuk)


@router.get("/commons/{parliamentdotuk}/votes/", response=list[VoteWithPersonSchema])
@paginate
@cache_crawled_data_view
def commons_division_votes(
    request: HttpRequest,
    parliamentdotuk: int,
    query: str = None,
    vote_type: DivisionVoteType = None,
):
    qs = DivisionVote.objects.commons(parliamentdotuk)
    if query:
        qs = qs.search(query)
    if vote_type:
        qs = qs.by_type(vote_type)
    return qs


@router.get("/lords/", response=list[DivisionMiniSchema])
@paginate
def lords_divisions(request: HttpRequest):
    return LordsDivision.objects.all()


@router.get("/lords/{parliamentdotuk}/", response=LordsDivisionSchema)
def lords_division(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(LordsDivision, parliamentdotuk=parliamentdotuk)


@router.get("/lords/{parliamentdotuk}/votes/", response=list[VoteWithPersonSchema])
@paginate
@cache_crawled_data_view
def lords_division_votes(
    request: HttpRequest,
    parliamentdotuk: int,
    query: str = None,
    vote_type: DivisionVoteType = None,
):
    qs = DivisionVote.objects.lords(parliamentdotuk)
    if query:
        qs = qs.search(query)
    if vote_type:
        qs = qs.by_type(vote_type)
    return qs
