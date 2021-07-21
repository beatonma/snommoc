from rest_framework.fields import SerializerMethodField

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
            "description",
            "address",
            "postcode",
            "phone",
            "fax",
            "email",
        ]


class _WebAddressSerializer(DetailedModelSerializer):
    class Meta:
        model = WebAddress
        fields = [
            "description",
            "url",
        ]


class AddressSerializer(DetailedModelSerializer):
    physical = _PhysicalAddressSerializer(many=True, source="physicaladdress_set")
    web = SerializerMethodField()

    class Meta:
        model = Person

        fields = [
            "physical",
            "web",
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
                    "description": "wikipedia_path",
                    "url": wiki,
                }
            ]

        return _WebAddressSerializer(links, many=True).data
