import logging

from django.http import HttpRequest
from ninja import Router, Schema
from ninja.pagination import paginate
from repository.models import Constituency, UnlinkedConstituency
from repository.resolution.constituency import resolve_unlinked_constituency

from .schema import (
    DashboardUnlinkedConstituencyDetailSchema,
    DashboardUnlinkedConstituencySchema,
)

log = logging.getLogger(__name__)
router = Router(tags=["Unlinked constituencies"])


@router.get(
    "unlinked/",
    response=list[DashboardUnlinkedConstituencySchema],
)
@paginate
def unlinked_constituencies(request: HttpRequest):
    return UnlinkedConstituency.objects.all().order_by("name", "election__date")


@router.get(
    "unlinked/{pk}/",
    response=DashboardUnlinkedConstituencyDetailSchema,
)
def unlinked_constituency(request: HttpRequest, pk: int):
    return UnlinkedConstituency.objects.get(pk=pk)


class ConfirmLinkedConstituencySchema(Schema):
    unlinked_id: int
    constituency_id: int


@router.post("confirm/")
def confirm_linked_constituency(
    request: HttpRequest,
    data: ConfirmLinkedConstituencySchema,
):
    try:
        unlinked = UnlinkedConstituency.objects.get(pk=data.unlinked_id)
        canonical_constituency = Constituency.objects.get(
            parliamentdotuk=data.constituency_id
        )
        resolve_unlinked_constituency(unlinked, canonical=canonical_constituency)

        return 204, None
    except Exception as e:
        log.warning(e)
        return 400, str(e)
