from api.pagination import offset_pagination
from api.schema.maps import ConstituencyMapSchema, PartyMapSchema
from django.http import HttpRequest
from ninja import Router
from ninja.pagination import paginate
from repository.models import Constituency, Party

router = Router(tags=["Maps"])


@router.get("/constituencies/", response=list[ConstituencyMapSchema])
@paginate(offset_pagination(50))
def constituencies(request: HttpRequest):
    return (
        Constituency.objects.current()
        .prefetch_related("boundary", "mp", "mp__party", "mp__party__theme")
        .order_by("-boundary__north")
    )


@router.get("/parties/", response=list[PartyMapSchema])
def parties(request: HttpRequest):
    return (
        Party.objects.current()
        .prefetch_related("territory")
        .order_by("-territory__north")
    )
