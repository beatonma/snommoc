"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedSerializer
from repository.models import (
    SubjectOfInterest,
    Person,
)

log = logging.getLogger(__name__)


class SubjectOfInterestSerializer(DetailedSerializer):
    category = serializers.CharField(source='category.title')

    class Meta:
        model = SubjectOfInterest
        fields = [
            'category',
            'subject',
        ]


class SubjectOfInterestCollectionSerializer(DetailedSerializer):
    subjects = SubjectOfInterestSerializer(many=True, source='subjectofinterest_set')

    class Meta:
        model = Person
        fields = [
            'subjects',
        ]
