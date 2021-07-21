from api.serializers.base import DetailedModelSerializer, InlineModelSerializer
from api.serializers.election import ElectionSerializer
from repository.models import Constituency
from repository.models import ConstituencyResult


class _MinimalConstituencySerializer(InlineModelSerializer):
    class Meta:
        model = Constituency
        fields = [
            "parliamentdotuk",
            "name",
        ]


class HistoricalConstituencySerializer(DetailedModelSerializer):
    constituency = _MinimalConstituencySerializer()
    election = ElectionSerializer()

    class Meta:
        model = ConstituencyResult
        fields = [
            "constituency",
            "start",
            "end",
            "election",
        ]
