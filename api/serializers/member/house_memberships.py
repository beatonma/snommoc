from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import HouseMembership


class HouseMembershipSerializer(DetailedModelSerializer):
    house = serializers.CharField(source="house.name")

    class Meta:
        model = HouseMembership
        fields = [
            "house",
            "start",
            "end",
        ]
