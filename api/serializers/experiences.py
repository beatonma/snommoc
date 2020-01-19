"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedSerializer
from repository.models import (
    Experience,
    Person,
)

log = logging.getLogger(__name__)


class ExperienceSerializer(DetailedSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Experience
        fields = [
            'category',
            'organisation',
            'title',
            'start',
            'end'
        ]


class ExperienceCollectionSerializer(DetailedSerializer):
    experiences = ExperienceSerializer(many=True, source='experience_set')

    class Meta:
        model = Person
        fields = [
            'experiences',
        ]
