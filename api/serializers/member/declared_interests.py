from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import DeclaredInterest


class DeclaredInterestSerializer(DetailedModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = DeclaredInterest
        fields = [
            "parliamentdotuk",
            "category",
            "description",
            "created",
            "amended",
            "deleted",
            "registered_late",
        ]
