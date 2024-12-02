from api.schema.bill import BillFullSchema
from api.schema.includes import BillMiniSchema
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from repository.models import Bill

router = Router(tags=["Bills"])


@router.get("/", response=list[BillMiniSchema])
@paginate
def bills(request: HttpRequest):
    return Bill.objects.all()


@router.get("/{parliamentdotuk}/", response=BillFullSchema)
def bill(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Bill, parliamentdotuk=parliamentdotuk)
