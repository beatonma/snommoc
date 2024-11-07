from api.schema.mini import PartyMiniSchema
from api.schema.party import PartyFullSchema
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Party

router = Router(tags=["Parties"])


@router.get("/", response=list[PartyMiniSchema])
@paginate
def parties(request: HttpRequest):
    return Party.objects.all()


@router.get("/{parliamentdotuk}/", response=PartyFullSchema)
def party(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Party, parliamentdotuk=parliamentdotuk)
