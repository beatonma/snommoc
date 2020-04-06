"""

"""

import logging

from api.serializers import DetailedModelSerializer
from repository.models import (
    PhysicalAddress,
    WebAddress,
    Person,
)

log = logging.getLogger(__name__)


class PhysicalAddressSerializer(DetailedModelSerializer):
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


class WebAddressSerializer(DetailedModelSerializer):
    class Meta:
        model = WebAddress
        fields = [
            'description',
            'url',
        ]


class AddressSerializer(DetailedModelSerializer):
    physical = PhysicalAddressSerializer(many=True, source='physicaladdress_set')
    web = WebAddressSerializer(many=True, source='webaddress_set')

    class Meta:
        model = Person

        fields = [
            'physical',
            'web',
        ]
