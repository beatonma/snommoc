from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import SubjectOfInterest


class SubjectOfInterestSerializer(DetailedModelSerializer):
    category = serializers.CharField(source="category.title")

    class Meta:
        model = SubjectOfInterest
        fields = [
            "category",
            "subject",
        ]
