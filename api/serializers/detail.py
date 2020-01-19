"""

"""

import logging

from rest_framework import serializers

from api.serializers.inline import InlineMemberSerializer
from repository.models import (
    Party,
    Constituency,
)

log = logging.getLogger(__name__)


class DetailedSerializer(serializers.HyperlinkedModelSerializer):
    """Return all details about the object."""
    pass


class PartySerializer(DetailedSerializer):
    class Meta:
        model = Party
        fields = [
            'name',
            'short_name',
            'long_name',
            'homepage',
            'year_founded',
            'wikipedia',
        ]


class ConstituencySerializer(DetailedSerializer):
    mp = InlineMemberSerializer()

    class Meta:
        model = Constituency
        fields = [
            'name',
            'mp',
            'start',
            'end',
        ]


