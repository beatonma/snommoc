from typing import List

from api.schema.person import MemberFullSchema, MemberMiniSchema
from ninja import Router
from ninja.pagination import paginate
from repository.models import Person

members_router = Router()


@members_router.get("/", response=List[MemberMiniSchema])
@paginate
def root(request):
    return Person.objects.filter(
        current_post__contains="Minister",
        party__name="Labour",
    ).select_related(
        "party",
        "constituency",
    )


@members_router.get("/{parliamentdotuk}/", response=MemberFullSchema)
def member(request, parliamentdotuk: int):
    return Person.objects.get(parliamentdotuk=parliamentdotuk)
