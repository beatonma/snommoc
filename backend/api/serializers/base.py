from django.http import HttpResponse
from rest_framework import (
    serializers,
    status,
)


class InlineModelSerializer(serializers.ModelSerializer):
    """Return basic data about the object with a link for further
    details if required."""

    pass


class DetailedModelSerializer(serializers.ModelSerializer):
    """Return all details about the object."""

    pass


class ReadOnlySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)

    def create(self, validated_data):
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
