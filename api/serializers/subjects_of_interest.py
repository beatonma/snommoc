"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedModelSerializer
from repository.models import (
    SubjectOfInterest,
    Person,
)

log = logging.getLogger(__name__)


class SubjectOfInterestSerializer(DetailedModelSerializer):
    category = serializers.CharField(source='category.title')

    class Meta:
        model = SubjectOfInterest
        fields = [
            'category',
            'subject',
        ]


class SubjectOfInterestCollectionSerializer(DetailedModelSerializer):
    subjects = SubjectOfInterestSerializer(many=True, source='subjectofinterest_set')

    class Meta:
        model = Person
        fields = [
            'subjects',
        ]
