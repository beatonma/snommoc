from api import contract
from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from api.serializers.election import ElectionSerializer
from repository.models import Constituency
from repository.models import ConstituencyResult


class _MinimalConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
        ]


class HistoricalConstituencySerializer(DetailedModelSerializer):
    constituency = _MinimalConstituencySerializer()
    election = ElectionSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            contract.CONSTITUENCY,
            contract.START,
            contract.END,
            contract.ELECTION,
        ]
