"""
Viewsets for any data about a particular member.
"""

import logging

from django.db.models import Q

from api.serializers.inline import InlineMemberSerializer
from api.serializers.profile import (
    SimpleProfileSerializer,
    FullProfileSerializer,
)
from api.serializers.votes import (
    MemberVotesSerializer,
    CommonsVotesSerializer,
    LordsVotesSerializer,
)
from api.views.viewsets import (
    KeyRequiredViewSet,
    Searchable,
)
from repository.models import (
    Constituency,
    Person,
    CommonsDivisionVote,
    LordsDivisionVote,
)
from surface.models import FeaturedPerson
from util.time import get_today

log = logging.getLogger(__name__)


class MemberViewSet(Searchable, KeyRequiredViewSet):
    """Member of Parliament: minimal, most important data.
    For more detail see [ProfileViewSet]"""

    queryset = Person.objects.all().prefetch_related("party", "constituency")

    search_fields = [
        "name",
        "current_post",
        "party__name",
        "constituency__name",
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SimpleProfileSerializer
        else:
            return InlineMemberSerializer


class BaseMemberViewSet(KeyRequiredViewSet):
    queryset = Person.objects.all()


class ProfileViewSet(BaseMemberViewSet):
    """Return detailed data about a person."""

    serializer_class = FullProfileSerializer


class FeaturedMembersViewSet(KeyRequiredViewSet):
    """Return a list of 'featured' people."""

    serializer_class = InlineMemberSerializer

    def get_queryset(self):
        today = get_today()
        qs = (
            FeaturedPerson.objects.filter(Q(start__isnull=True) | Q(start__lte=today))
            .filter(Q(end__isnull=True) | Q(end__gte=today))
            .select_related("target")
        )
        return [item.target for item in qs]


class MemberVotesViewSet(BaseMemberViewSet):
    serializer_class = MemberVotesSerializer


class _MemberHouseVotesViewSet(KeyRequiredViewSet):
    """Abstract class for showing votes by a member in a specific house."""

    model = None

    def retrieve(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return (
            self.model.objects.filter(
                person=self.kwargs.get("pk"),
            )
            .prefetch_related("division")
            .order_by("-division__date")
        )


class MemberCommonsVotesViewSet(_MemberHouseVotesViewSet):
    serializer_class = CommonsVotesSerializer
    model = CommonsDivisionVote


class MemberLordsVotesViewSet(_MemberHouseVotesViewSet):
    serializer_class = LordsVotesSerializer
    model = LordsDivisionVote


class MemberForConstituencyViewSet(BaseMemberViewSet):
    serializer_class = InlineMemberSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        try:
            return Constituency.objects.get(parliamentdotuk=pk).mp

        except Exception as e:
            log.warning(f"Unable to retrieve MP for constituency={pk}: {e}")
