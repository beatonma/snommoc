"""
Viewsets for any data about a particular member.
"""

import logging

from django.db.models import Q

from api.serializers import (
    InlineMemberSerializer,
    InlinePartySerializer,
    SimpleProfileSerializer,
    PartySerializer,
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
    Party,
    Person,
    CommonsDivisionVote,
    LordsDivisionVote,
)
from surface.models import FeaturedPerson
from util.time import get_today

log = logging.getLogger(__name__)


class PartyViewSet(Searchable, KeyRequiredViewSet):
    """Political party."""

    queryset = Party.objects.all()

    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PartySerializer
        else:
            return InlinePartySerializer


class MemberViewSet(Searchable, KeyRequiredViewSet):
    """Member of Parliament."""

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
    """Return all data about a person.

    Please see individual endpoints for documentation.

    Fields:

      - `profile`
        - `parliamentdotuk`: Person ID as used on parliament.uk API
        - `name`: Full name
        - `full_title`: Full title with honorifics
        - `given_name`: Simple first name
        - `family_name`: Simple surname
        - `active`: Whether this person is currently a member of parliament
        - `theyworkforyou`: Person ID as used on theyworkforyou.com API
        - `party`: Current party association
        - `constituency`: Current constituency represented by this Person
        - `is_mp`: Whether this person is a current MP
        - `is_lord`: Whether this person is a current Lord
        - `date_of_birth`: When this person was born
        - `date_of_death`: When this person died, if they have passed
        - `age`: The person's current age, or age at time of death if they have passed
        - `gender`: This person's 'registered' gender
        - `place_of_birth`: Town and country of birth
            - `town`
            - `country`
      - `address`
      - `committees`
      - `constituencies`
      - `experiences`
      - `houses`
      - `interests`
      - `speeches`
      - `parties`
      - `posts`
      - `subjects`
    """

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


class MemberHouseVotesViewSet(KeyRequiredViewSet):
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


class MemberCommonsVotesViewSet(MemberHouseVotesViewSet):
    serializer_class = CommonsVotesSerializer
    model = CommonsDivisionVote


class MemberLordsVotesViewSet(MemberHouseVotesViewSet):
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
