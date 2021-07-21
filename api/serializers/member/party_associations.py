from api.serializers.base import DetailedModelSerializer
from api.serializers.parties import InlinePartySerializer
from repository.models import PartyAssociation


class HistoricalPartySerializer(DetailedModelSerializer):
    party = InlinePartySerializer()

    class Meta:
        model = PartyAssociation
        fields = [
            "party",
            "start",
            "end",
        ]
