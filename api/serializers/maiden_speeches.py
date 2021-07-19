import logging

from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import (
    MaidenSpeech,
    Person,
)

log = logging.getLogger(__name__)


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


class MaidenSpeechCollectionSerializer(DetailedModelSerializer):
    maiden_speeches = MaidenSpeechSerializer(many=True, source="maidenspeech_set")

    class Meta:
        model = Person
        fields = [
            "maiden_speeches",
        ]
