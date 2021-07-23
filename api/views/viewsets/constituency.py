from django.http import Http404

from api.serializers.constituencies import ConstituencySerializer
from api.serializers.constituencies.election_results import (
    ConstituencyResultDetailsSerializer,
)
from api.serializers.inline import InlineConstituencySerializer
from api.views.viewsets import (
    KeyRequiredViewSet,
    Searchable,
)
from repository.models import (
    Constituency,
    ConstituencyResultDetail,
)


class ConstituencyViewSet(Searchable, KeyRequiredViewSet):
    """Parliamentary constituency."""

    queryset = Constituency.objects.all()
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConstituencySerializer
        else:
            return InlineConstituencySerializer


class ConstituencyResultDetailViewSet(KeyRequiredViewSet):
    serializer_class = ConstituencyResultDetailsSerializer

    def get_object(self):
        constituency_id = self.kwargs.get("pk")
        election_id = self.kwargs.get("election_id")

        obj = ConstituencyResultDetail.objects.filter(
            constituency_result__constituency__parliamentdotuk=constituency_id,
            constituency_result__election__parliamentdotuk=election_id,
        ).first()

        if obj:
            return obj

        else:
            raise Http404
