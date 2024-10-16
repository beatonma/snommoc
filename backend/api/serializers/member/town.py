from rest_framework import serializers

from api import contract
from api.serializers.base import InlineModelSerializer

from repository.models import Town


class TownSerializer(InlineModelSerializer):
    town = serializers.CharField(source="name")
    country = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Town
        fields = [
            contract.TOWN,
            contract.COUNTRY,
        ]
