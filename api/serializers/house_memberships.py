"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedSerializer
from repository.models import HouseMembership

log = logging.getLogger(__name__)


class HouseMembershipSerializer(DetailedSerializer):
    house = serializers.CharField(source='house.name')

    class Meta:
        model = HouseMembership
        fields = [
            'house',
            'start',
            'end',
        ]
