import logging

from api.schema.member import MemberCareerHistory, MemberProfile, MemberVotesSchema
from api.schema.mini import MemberMiniSchema
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import CommonsDivisionVote, LordsDivisionVote, Person

log = logging.getLogger(__name__)
router = Router(tags=["Members"])


@router.get("/", response=list[MemberMiniSchema])
@paginate
def members(request: HttpRequest, query: str = None):
    qs = Person.objects.all().select_related("party", "constituency")

    if not query:
        return qs.filter(active=True)

    return qs.filter(name__icontains=query).order_by("active", "-pk")


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
