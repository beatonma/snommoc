"""

"""

import logging

from api.serializers import (
    DetailedSerializer,
    InlinePartySerializer,
)
from repository.models import (
    Party,
    Person,
    PartyAssociation,
)

log = logging.getLogger(__name__)


class PartySerializer(DetailedSerializer):
    class Meta:
        model = Party
        fields = [
            'name',
            'short_name',
            'long_name',
            'homepage',
            'year_founded',
            'wikipedia',
        ]


class HistoricalPartySerializer(DetailedSerializer):
    party = InlinePartySerializer()

    class Meta:
        model = PartyAssociation
        fields = [
            'party',
            'start',
            'end',
        ]


class HistoricalPartyCollectionSerializer(DetailedSerializer):
    parties = HistoricalPartySerializer(many=True)

    class Meta:
        model = Person
        fields = [
            'parties',
        ]
