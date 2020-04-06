"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedModelSerializer
from repository.models import (
    DeclaredInterest,
    Person,
)

log = logging.getLogger(__name__)


class DeclaredInterestSerializer(DetailedModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = DeclaredInterest
        fields = [
            'parliamentdotuk',
            'category',
            'description',
            'created',
            'amended',
            'deleted',
            'registered_late',
        ]


class DeclaredInterestCollectionSerializer(DetailedModelSerializer):
    interests = DeclaredInterestSerializer(many=True, source='declaredinterest_set')

    class Meta:
        model = Person
        fields = [
            'interests',
        ]
