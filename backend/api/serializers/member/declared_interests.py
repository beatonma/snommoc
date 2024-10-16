from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer
from repository.models import DeclaredInterest


class DeclaredInterestSerializer(DetailedModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = DeclaredInterest
        fields = [
            contract.PARLIAMENTDOTUK,
            contract.CATEGORY,
            contract.DESCRIPTION,
            contract.INTEREST_CREATED,
            contract.INTEREST_AMENDED,
            contract.INTEREST_DELETED,
            contract.INTEREST_LATE,
        ]
