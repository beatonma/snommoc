from rest_framework.fields import SerializerMethodField

from api import contract
from api.serializers.base import DetailedModelSerializer
from repository.models import (
    PhysicalAddress,
    WebAddress,
    Person,
)


class _PhysicalAddressSerializer(DetailedModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = [
            contract.DESCRIPTION,
            contract.ADDRESS,
            contract.POSTCODE,
            contract.PHONE,
            contract.FAX,
            contract.EMAIL,
        ]


class _WebAddressSerializer(DetailedModelSerializer):
    class Meta:
        model = WebAddress
        fields = [
            contract.DESCRIPTION,
            contract.URL,
        ]


class AddressSerializer(DetailedModelSerializer):
    physical = _PhysicalAddressSerializer(many=True, source="physicaladdress_set")
    web = SerializerMethodField()

    class Meta:
        model = Person

        fields = [
            contract.ADDRESS_PHYSICAL,
            contract.ADDRESS_WEB,
        ]

    def get_web(self, obj):
        """
        Related WebAddress instances with partial Wikipedia path, if available.
        Full url needs to be constructed by client (where they can apply localisation as required).
        """
        wiki = obj.wikipedia
        links = obj.webaddress_set
        if wiki:
            links = list(links.values()) + [
                {
                    contract.DESCRIPTION: contract.WIKIPEDIA_PATH,
                    contract.URL: wiki,
                }
            ]

        return _WebAddressSerializer(links, many=True).data
