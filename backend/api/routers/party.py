from api.schema.includes import PartyMiniSchema
from api.schema.party import PartyFullSchema
from django.db.models import F, Q, Sum
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Party

router = Router(tags=["Parties"])


@router.get("/", response=list[PartyMiniSchema])
@paginate
def parties(request: HttpRequest, query: str = None):
    qs = Party.objects.all().prefetch_related("gender_demographics")

    if query:
        qs = qs.search(query)

    qs = qs.annotate(
        active_commons_members=Sum(
            "gender_demographics__total_member_count",
            filter=Q(gender_demographics__house__name="Commons"),
        )
    )
    ordering = [
        F("active_commons_members").desc(nulls_last=True),
        F("active_member_count").desc(nulls_last=True),
        "name",
    ]
    return qs.order_by(*ordering)


@router.get("/{parliamentdotuk}/", response=PartyFullSchema)
def party(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Party, parliamentdotuk=parliamentdotuk)
