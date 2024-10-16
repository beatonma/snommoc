from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from repository.models import MaidenSpeech


class MaidenSpeechSerializer(DetailedModelSerializer):
    house = serializers.CharField(source="house.name")

    class Meta:
        model = MaidenSpeech
        fields = [
            contract.HOUSE,
            contract.DATE,
            contract.SUBJECT,
            contract.HANSARD,
        ]
