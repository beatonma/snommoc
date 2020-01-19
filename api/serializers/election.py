"""

"""

import logging

from rest_framework import serializers

from api.serializers import DetailedSerializer
from repository.models import Election

log = logging.getLogger(__name__)


class ElectionSerializer(DetailedSerializer):
    election_type = serializers.CharField(source='election_type.name')

    class Meta:
        model = Election
        fields = [
            'parliamentdotuk',
            'name',
            'date',
            'election_type',
        ]
