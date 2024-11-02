from api.schema.division import CommonsDivisionSchema, LordsDivisionSchema
from api.schema.mini import DivisionMiniSchema
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import CommonsDivision, LordsDivision

router = Router(tags=["Divisions"])


@router.get("/commons/", response=list[DivisionMiniSchema])
@paginate
def commons_divisions(request: HttpRequest):
    return CommonsDivision.objects.all()


@router.get("/commons/{parliamentdotuk}/", response=CommonsDivisionSchema)
def commons_division(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(CommonsDivision, parliamentdotuk=parliamentdotuk)


@router.get("/lords/", response=list[DivisionMiniSchema])
@paginate
def lords_divisions(request: HttpRequest):
    return LordsDivision.objects.all()


@router.get("/lords/{parliamentdotuk}/", response=LordsDivisionSchema)
def lords_division(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(LordsDivision, parliamentdotuk=parliamentdotuk)
