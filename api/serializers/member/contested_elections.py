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
            "election",
            "constituency",
        ]


class ContestedElectionCollectionSerializer(UnusedClass, DetailedModelSerializer):
    contested = _ContestedElectionSerializer(many=True, source="contestedelection_set")

    class Meta:
        model = Person
        fields = [
            "contested",
        ]
