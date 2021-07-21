from rest_framework import serializers

from api.serializers.base import DetailedModelSerializer

from repository.models import ConstituencyBoundary


class ConstituencyBoundarySerializer(DetailedModelSerializer):
    kml = serializers.CharField(source="boundary_kml")

    class Meta:
        model = ConstituencyBoundary
        fields = [
            "kml",
            "center_latitude",
            "center_longitude",
            "area",
            "boundary_length",
        ]
