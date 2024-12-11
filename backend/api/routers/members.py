import logging
from typing import Literal

from api.schema.includes import MemberMiniSchema
from api.schema.member import MemberCareerHistory, MemberProfile, MemberVotesSchema
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import CommonsDivisionVote, LordsDivisionVote, Person
from repository.models.houses import HouseType
from util.collections import all_none

log = logging.getLogger(__name__)
router = Router(tags=["Members"])

type StatusFilter = Literal["current", "inactive", "historical", "all"]


@router.get("/", response=list[MemberMiniSchema])
@paginate
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
        qs = qs.filter(party__parliamentdotuk=party)

    if house:
        qs = qs.filter(house__name__iexact=house)

    if not query:
        return qs.order_by("sort_name")

    return qs.filter(
        Q(name__icontains=query) | Q(constituency__name__icontains=query)
    ).order_by("status__is_active", "sort_name")


@router.get("/{parliamentdotuk}/", response=MemberProfile)
def member(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Person, parliamentdotuk=parliamentdotuk)


@router.get("/{parliamentdotuk}/career/", response=MemberCareerHistory)
def member_career(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Person, parliamentdotuk=parliamentdotuk)


@router.get("/{parliamentdotuk}/votes/", response=MemberVotesSchema)
def member_votes(request: HttpRequest, parliamentdotuk: int):
    person = get_object_or_404(Person, parliamentdotuk=parliamentdotuk)

    commons = CommonsDivisionVote.objects.for_member(person)
    lords = LordsDivisionVote.objects.for_member(person)

    return {
        "commons": commons,
        "lords": lords,
    }
