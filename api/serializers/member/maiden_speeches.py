from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import MaidenSpeech


class MaidenSpeechSerializer(DetailedModelSerializer):
    house = serializers.CharField(source="house.name")

    class Meta:
        model = MaidenSpeech
        fields = [
            "house",
            "date",
            "subject",
            "hansard",
        ]
