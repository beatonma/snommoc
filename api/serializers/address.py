"""

"""

import logging

from api.serializers import DetailedSerializer
from repository.models import (
    PhysicalAddress,
    WebAddress,
    Person,
)

log = logging.getLogger(__name__)


class PhysicalAddressSerializer(DetailedSerializer):
    class Meta:
        model = PhysicalAddress
        fields = [
            'description',
            'address',
            'postcode',
            'phone',
            'fax',
            'email',
        ]


class WebAddressSerializer(DetailedSerializer):
    class Meta:
        model = WebAddress
        fields = [
            'description',
            'url',
        ]


class AddressSerializer(DetailedSerializer):
    physical = PhysicalAddressSerializer(many=True, source='physicaladdress_set')
    web = WebAddressSerializer(many=True, source='webaddress_set')

    class Meta:
        model = Person

        fields = [
            'physical',
            'web',
        ]
