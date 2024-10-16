from api.serializers.parties import (
    PartySerializer,
    InlinePartySerializer,
)
from api.views.viewsets import (
    Searchable,
    KeyRequiredViewSet,
)
from repository.models import Party


class PartyViewSet(Searchable, KeyRequiredViewSet):
    """Political party: basic info."""

    queryset = Party.objects.all()

    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PartySerializer
        else:
            return InlinePartySerializer
