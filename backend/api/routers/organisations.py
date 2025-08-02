from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from api.cache import cache_crawled_data_view
from api.schema.includes import OrganisationSchema
from repository.models import Organisation

router = Router(tags=["Organisations"])


@router.get("/", response=list[OrganisationSchema])
@paginate
@cache_crawled_data_view
def organisations(request: HttpRequest, query: str = None):
    qs = Organisation.objects.all()

    if query:
        qs = qs.search(query)

    return qs


@router.get("/{slug}/", response=OrganisationSchema)
def organisation(request: HttpRequest, slug: str):
    return get_object_or_404(Organisation, slug=slug)
