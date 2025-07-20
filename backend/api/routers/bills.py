from api.cache import cache_crawled_data_view
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
@cache_crawled_data_view
def bills(request: HttpRequest, query: str = None):
    qs = Bill.objects.all()

    if query:
        qs = qs.search(query)

    return qs


@router.get("/{parliamentdotuk}/", response=BillFullSchema)
def bill(request: HttpRequest, parliamentdotuk: int):
    return get_object_or_404(Bill, parliamentdotuk=parliamentdotuk)
