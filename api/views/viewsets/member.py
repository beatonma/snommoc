"""
Viewsets for any data about a particular member.
"""

import logging

from api.serializers.inline import InlineMemberSerializer
from api.serializers.member import FullProfileSerializer
from api.serializers.member.votes import MemberVotesSerializer
from api.views.viewsets import (
    KeyRequiredViewSet,
    Searchable,
)
from repository.models import Person

log = logging.getLogger(__name__)


class _BaseMemberViewSet(KeyRequiredViewSet):
    queryset = Person.objects.all()


class MemberViewSet(Searchable, KeyRequiredViewSet):
    """Member of Parliament: minimal, most important data.
    For more detail see [ProfileViewSet]"""

    serializer_class = InlineMemberSerializer
    queryset = Person.objects.all().prefetch_related("party", "constituency")

    search_fields = [
        "name",
        "current_post",
        "party__name",
        "constituency__name",
    ]


class ProfileViewSet(_BaseMemberViewSet):
    """Return detailed data about a person."""

    serializer_class = FullProfileSerializer


class MemberVotesViewSet(_BaseMemberViewSet):
    serializer_class = MemberVotesSerializer
