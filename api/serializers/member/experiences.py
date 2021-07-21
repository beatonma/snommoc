from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer
from repository.models import Experience


class ExperienceSerializer(DetailedModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Experience
        fields = [
            "category",
            "organisation",
            "title",
            "start",
            "end",
        ]
