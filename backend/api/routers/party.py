from api.schema.mini import PartyMiniSchema
from api.schema.party import PartyFullSchema
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Party

router = Router(tags=["Parties"])


@router.get("/", response=list[PartyMiniSchema])
@paginate
def parties(request: HttpRequest, query: str = None):
    qs = Party.objects.all()

    if query:
        return qs.filter(
            Q(name__icontains=query)
            | Q(short_name__icontains=query)
            | Q(long_name__icontains=query)
        )

    return qs


@router.get("/{parliamentdotuk}/", response=PartyFullSchema)
def party(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Party, parliamentdotuk=parliamentdotuk)
