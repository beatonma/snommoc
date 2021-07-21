from api import contract
from api.serializers.election import ElectionSerializer
from repository.models import Person, ContestedElection
from api.serializers.base import DetailedModelSerializer
from api.serializers.inline import InlineConstituencySerializer
from util.cleanup import UnusedClass


class _ContestedElectionSerializer(DetailedModelSerializer):
    election = ElectionSerializer()
    constituency = InlineConstituencySerializer()

    class Meta:
        model = ContestedElection
        fields = [
            contract.ELECTION,
            contract.CONSTITUENCY,
        ]


class ContestedElectionCollectionSerializer(UnusedClass, DetailedModelSerializer):
    contested = _ContestedElectionSerializer(many=True, source="contestedelection_set")

    class Meta:
        model = Person
        fields = [
            contract.CONTESTED_ELECTION,
        ]
