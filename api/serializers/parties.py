from api import contract
from api.serializers.base import (
    DetailedModelSerializer,
    InlineModelSerializer,
)

from repository.models import Party


class InlinePartySerializer(InlineModelSerializer):
    class Meta:
        model = Party
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
        ]


class PartySerializer(DetailedModelSerializer):
    class Meta:
        model = Party
        fields = [
            contract.NAME,
            contract.PARTY_SHORT_NAME,
            contract.PARTY_LONG_NAME,
            contract.PARTY_HOMEPAGE,
            contract.PARTY_YEAR_FOUNDED,
            contract.PARTY_WIKIPEDIA,
        ]
