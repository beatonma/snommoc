from django.db.models import Count, F, Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from api.cache import cache_crawled_data_view
from api.schema.includes import PartyMiniSchema
from api.schema.party import PartyFullSchema
from repository.models import Party
from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS

router = Router(tags=["Parties"])


@router.get("/", response=list[PartyMiniSchema])
@paginate
@cache_crawled_data_view
def parties(request: HttpRequest, query: str = None):
    qs = Party.objects.all().prefetch_related("person_set")

    if query:
        qs = qs.search(query)

    active_member_kwargs = {"person__status__is_active": True}

    qs = qs.annotate(
        active_mp_count=Count(
            "person",
            filter=Q(**active_member_kwargs, person__house__name=HOUSE_OF_COMMONS),
        ),
        active_lord_count=Count(
            "person",
            filter=Q(**active_member_kwargs, person__house__name=HOUSE_OF_LORDS),
        ),
    )

    return qs.order_by(F("active_mp_count").desc(), F("active_lord_count").desc())


@router.get("/{parliamentdotuk}/", response=PartyFullSchema)
def party(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(
        Party.objects.all().prefetch_related("person_set"),
        parliamentdotuk=parliamentdotuk,
    )
