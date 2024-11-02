from api.schema.election import ElectionSchema
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Election

router = Router(tags=["Elections"])


@router.get("/", response=list[ElectionSchema])
@paginate
def elections(request: HttpRequest):
    return Election.objects.all()


@router.get("/{parliamentdotuk}/", response=ElectionSchema)
def election(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Election, parliamentdotuk=parliamentdotuk)
