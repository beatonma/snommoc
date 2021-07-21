from api.serializers.base import (
    DetailedModelSerializer,
    InlineModelSerializer,
)

from repository.models import Party


class InlinePartySerializer(InlineModelSerializer):
    class Meta:
        model = Party
        fields = [
            "parliamentdotuk",
            "name",
        ]


class PartySerializer(DetailedModelSerializer):
    class Meta:
        model = Party
        fields = [
            "name",
            "short_name",
            "long_name",
            "homepage",
            "year_founded",
            "wikipedia",
        ]
