"""
Viewsets for any data about a particular member.
"""

import logging
import datetime

from django.db.models import Q

from api.serializers import (
    ConstituencySerializer,
    InlineConstituencySerializer,
    InlineMemberSerializer,
    InlinePartySerializer,
    SimpleProfileSerializer,
    PartySerializer,
    FullProfileSerializer,
)
from api.serializers.votes import MemberVotesSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Constituency,
    Party,
    Person,
)
from surface.models import FeaturedPerson

log = logging.getLogger(__name__)


class PartyViewSet(KeyRequiredViewSet):
    """Political party."""
    queryset = Party.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PartySerializer
        else:
            return InlinePartySerializer


class ConstituencyViewSet(KeyRequiredViewSet):
    """Parliamentary constituency."""
    queryset = Constituency.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ConstituencySerializer
        else:
            return InlineConstituencySerializer


class MemberViewSet(KeyRequiredViewSet):
    """Member of Parliament."""
    queryset = Person.objects.all() \
        .prefetch_related('party', 'constituency')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SimpleProfileSerializer
        else:
            return InlineMemberSerializer


class BaseMemberViewSet(KeyRequiredViewSet):
    queryset = Person.objects.all()


# class AddressViewSet(BaseMemberViewSet):
#     """Physical and web addresses for a Person.
#
#     Fields:
#
#       - `physical`: List of physical addresses
#         - `description`: What kind of address is this e.g. Parliament, constituency
#         - `address`: The address as it would appear on an envelope (excluding postcode)
#         - `postcode`: The postcode for this address
#         - `phone`: Phone number for this address
#         - `fax`: Fax number for this address
#         - `email`: Email address associated with this address.
#       - `web`: List of web addresses
#         - `description`: e.g. website, Twitter, etc
#         - `url`: Link to the thing
#     """
#     serializer_class = AddressSerializer
#
#
# class CommitteeViewSet(BaseMemberViewSet):
#     """Committee membership for a Person.
#
#     Fields:
#
#       - `parliamentdotuk`: Committee ID used on parilament.uk API
#       - `name`: Name of the committee
#       - `start`: When the Person joined the committee
#       - `end`: When the Person left the committee
#       - `chair` [list]:
#         - `start`: When the Person became Chair of the committee
#         - `end`: When the Person stopped being Chair of the committee
#     """
#     serializer_class = CommitteeSerializer
#
#
# class ContestedElectionViewSet(BaseMemberViewSet):
#     """Elections in which the Person ran but did not win.
#
#     Fields:
#
#     - `election`:
#         - `parliamentdotuk`: election ID used on parliament.uk API
#         - `name`: Name of the election
#         - `date`: When the election occurred
#         - `election_type`: e.g. General Election, special election, etc
#
#     - `constituency`:
#         - `name`: Name of the constituency that was contested
#         - `detail_url`: Link to more details about this constituency.
#
#     """
#     serializer_class = ContestedElectionCollectionSerializer
#
#
# class DeclaredInterestViewSet(BaseMemberViewSet):
#     """Declared interests for a Person.
#
#     Registered financial interests of a Person.
#
#     Fields:
#
#     - `parliamentdotuk`: ID used on parliament.uk API
#     - `category`: e.g. Land/property ownership, shareholdings, directorships, etc
#     - `description`: Description of the interest.
#     - `created`: When the interest was registered
#     - `amended`: When the interest was last updated, or null if never updated
#     - `deleted`: When the interest was removed, or null if never removed
#     - `registered_late`: Whether this interest was registered later than expected(?)
#
#     """
#     serializer_class = DeclaredInterestCollectionSerializer
#
#
# class ElectionViewSet(BaseMemberViewSet):
#     serializer_class = ElectionSerializer
#
#
# class ExperienceViewSet(BaseMemberViewSet):
#     """Experience entries for a Person.
#
#     Experiences typically represent positions of power that a Person
#     has held outside of parliament but could potentially be important to
#     their actions within parliament. These positions may be political or
#     otherwise in nature.
#
#     Fields:
#
#       - `category`:       Political/Non political
#       - `organisation`:   Name of the organisation involved
#       - `title`:          Name of the position within that organisation
#       - `start`:          When the Person started the job
#       - `end`:            When the Person left the job. May be null if they
#                           are still involved.
#
#     Note: `start`/`end` dates that are listed as `yyyy-12-25`
#           mean that the event happened during the given year, not that it
#           happened on Christmas day.
#     """
#     serializer_class = ExperienceCollectionSerializer
#
#
# class HistoricalConstituencyViewSet(BaseMemberViewSet):
#     """Historical constituencies for a Person.
#
#     Fields:
#
#       - `constituency`:
#         - `parliamentdotuk`: Constituency ID used on parliament.uk API
#         - `name`: Name of the constituency
#
#       - `start`: When this Person represented the constituency from
#       - `end`: When this Person represented the constituency until
#       - `election`:
#         - `parliamentdotuk`: election ID used on parliament.uk API
#         - `name`: Name of the election
#         - `date`: When the election occurred
#         - `election_type`: e.g. General Election, special election, etc
#     """
#     serializer_class = HistoricalConstituencyCollectionSerializer
#
#
# class HistoricalPartyViewSet(BaseMemberViewSet):
#     """Historical party associations for a Person.
#
#     Fields:
#
#       - `party`:
#         - `name`: Name of the party
#         - `detail_url`: Link to full Party details
#
#       - `start`: When this party association began
#       - `end`: When this party association ended
#     """
#     serializer_class = HistoricalPartyCollectionSerializer
#
#
# class MaidenSpeechViewSet(BaseMemberViewSet):
#     """Maiden speeches for a Person.
#
#     Fields:
#
#       - `house`: Where the speech took place - Commons/Lords
#       - `date`: When the speech happened
#       - `subject`: What the speech was about
#       - `hansard`: Identifier used in Hansard records
#     """
#     serializer_class = MaidenSpeechCollectionSerializer
#
#
# class PostViewSet(BaseMemberViewSet):
#     """Governmental, Parliamentary, Opposition posts for a Person.
#
#     Each post type has the same structure.
#
#     Fields:
#
#       - `governmental`
#         - `parliamentdotuk`: Post ID as used on parliament.uk API
#         - `name`: Name of the post
#         - `hansard`: Name of the post as used in Hansard records
#       - `parliamentary`
#         - `parliamentdotuk`: Post ID as used on parliament.uk API
#         - `name`: Name of the post
#         - `hansard`: Name of the post as used in Hansard records
#       - `opposition`
#         - `parliamentdotuk`: Post ID as used on parliament.uk API
#         - `name`: Name of the post
#         - `hansard`: Name of the post as used in Hansard records
#     """
#     serializer_class = AllPostSerializer
#
#
# class SubjectOfInterestViewSet(BaseMemberViewSet):
#     """Return a Person's subjects of interest.
#
#     Fields:
#       - `category`: Short description of category
#       - `subject`: Plain text description of interests
#     """
#     serializer_class = SubjectOfInterestCollectionSerializer
#
#
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
        today = datetime.date.today()
        qs = FeaturedPerson.objects.filter(
            Q(start__isnull=True) | Q(start__lte=today)
        ).filter(
            Q(end__isnull=True) | Q(end__gte=today)
        ).select_related('person')
        return [item.person for item in qs]


class MemberCommonsVotesViewSet(BaseMemberViewSet):
    serializer_class = MemberVotesSerializer
