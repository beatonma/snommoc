"""

"""

import logging

from rest_framework import serializers

from api.serializers import (
    DetailedModelSerializer,
    InlineConstituencySerializer,
)
from api.serializers.election import ElectionSerializer
from repository.models import Person
from repository.models.election import ContestedElection

log = logging.getLogger(__name__)


class ContestedElectionSerializer(DetailedModelSerializer):
    # election = serializers.CharField(source='election.name')
    election = ElectionSerializer()
    constituency = InlineConstituencySerializer()

    class Meta:
        model = ContestedElection
        fields = [
            'election',
            'constituency',
        ]


class ContestedElectionCollectionSerializer(DetailedModelSerializer):
    contested = ContestedElectionSerializer(many=True, source='contestedelection_set')

    class Meta:
        model = Person
        fields = [
            'contested',
        ]
