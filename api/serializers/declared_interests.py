"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedSerializer
from repository.models import (
    DeclaredInterest,
    Person,
)

log = logging.getLogger(__name__)


class DeclaredInterestSerializer(DetailedSerializer):
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


class DeclaredInterestCollectionSerializer(DetailedSerializer):
    interests = DeclaredInterestSerializer(many=True, source='declaredinterest_set')

    class Meta:
        model = Person
        fields = [
            'interests',
        ]
