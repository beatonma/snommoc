from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from repository.models import Election


class ElectionSerializer(DetailedModelSerializer):
    election_type = serializers.CharField(source="election_type.name")

    class Meta:
        model = Election
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.NAME,
            contract.DATE,
            contract.ELECTION_TYPE,
        ]
