import logging
from typing import Literal

from api.cache import cache_crawled_data_view
from api.schema.includes import MemberMiniSchema
from api.schema.member import DivisionWithVoteSchema, MemberCareerHistory, MemberProfile
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Person
from repository.models.houses import HouseType
from util.collections import all_none

log = logging.getLogger(__name__)
router = Router(tags=["Members"])

type StatusFilter = Literal["current", "inactive", "historical", "all"]


@router.get("/", response=list[MemberMiniSchema])
@paginate
@cache_crawled_data_view
def members(
    request: HttpRequest,
    query: str = None,
    party: int = None,
    house: HouseType | None = None,
    status: StatusFilter | None = None,
):
    qs = Person.objects.all().select_related("party", "constituency")

    if not query and all_none(party, house, status):
        return qs.current().order_by("sort_name")

    if status is None or status == "current":
        qs = qs.current()
    elif status == "inactive":
        qs = qs.inactive()
    elif status == "historical":
        qs = qs.historical()

    if party:
        qs = qs.for_party_id(party)

    if house:
        qs = qs.for_house(house)

    if not query:
        return qs.order_by("sort_name")

    return qs.search(query).order_by("status__is_active", "sort_name")


@router.get("/{parliamentdotuk}/", response=MemberProfile)
def member(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Person, parliamentdotuk=parliamentdotuk)


@router.get("/{parliamentdotuk}/career/", response=MemberCareerHistory)
def member_career(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Person, parliamentdotuk=parliamentdotuk)


@router.get("/{parliamentdotuk}/votes/", response=list[DivisionWithVoteSchema])
@paginate
@cache_crawled_data_view
def member_votes(request: HttpRequest, parliamentdotuk: int, query: str = None):
    person = get_object_or_404(Person, parliamentdotuk=parliamentdotuk)

    qs = person.votes.all()
    if query:
        qs = qs.filter(division__title__icontains=query)

    return qs

    # commons_qs = person.commons_votes.all()
    # lords_qs = person.lords_votes.all()
    #
    # if query:
    #     commons_qs = commons_qs.filter(division__title__icontains=query)
    #     lords_qs = lords_qs.filter(division__title__icontains=query)
    #
    # return sorted(
    #     chain(commons_qs, lords_qs), key=lambda x: x.division.date, reverse=True
    # )
