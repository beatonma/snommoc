import logging

from api.serializers.base import DetailedModelSerializer, InlineModelSerializer

from repository.models import (
    Party,
    Person,
    PartyAssociation,
)

log = logging.getLogger(__name__)


class InlinePartySerializer(InlineModelSerializer):
    class Meta:
        model = Party
        fields = [
            "parliamentdotuk",
            "name",
        ]


class PartySerializer(DetailedModelSerializer):
    class Meta:
        model = Party
        fields = [
            "name",
            "short_name",
            "long_name",
            "homepage",
            "year_founded",
            "wikipedia",
        ]


class HistoricalPartySerializer(DetailedModelSerializer):
    party = InlinePartySerializer()

    class Meta:
        model = PartyAssociation
        fields = [
            "party",
            "start",
            "end",
        ]


class HistoricalPartyCollectionSerializer(DetailedModelSerializer):
    parties = HistoricalPartySerializer(many=True)

    class Meta:
        model = Person
        fields = [
            "parties",
        ]
