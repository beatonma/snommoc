from rest_framework import serializers

from api import contract
from api.serializers.base import DetailedModelSerializer

from repository.models import ConstituencyBoundary


class ConstituencyBoundarySerializer(DetailedModelSerializer):
    kml = serializers.CharField(source="boundary_kml")

    class Meta:
        model = ConstituencyBoundary
        fields = [
            contract.CONSTITUENCY_BOUNDARY_KML,
            contract.CONSTITUENCY_BOUNDARY_CENTER_LATITUDE,
            contract.CONSTITUENCY_BOUNDARY_CENTER_LONGITUDE,
            contract.CONSTITUENCY_BOUNDARY_AREA,
            contract.CONSTITUENCY_BOUNDARY_LENGTH,
        ]
