from api.serializers.divisions import (
    CommonsDivisionSerializer,
    LordsDivisionSerializer,
)
from api.serializers.divisions.votes import GenericInlineDivisionSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import CommonsDivision, LordsDivision
from util.cleanup import UnusedClass


class CommonsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Commons division, including vote results."""

    queryset = CommonsDivision.objects.all()
    serializer_class = CommonsDivisionSerializer


class LordsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Lords division, including vote results."""

    queryset = LordsDivision.objects.all()
    serializer_class = LordsDivisionSerializer


class RecentlyUpdatedDivisionsViewSet(UnusedClass, KeyRequiredViewSet):
    serializer_class = GenericInlineDivisionSerializer

    def get_queryset(self):
        commons = CommonsDivision.objects.order_by("-date")[:10]
        lords = LordsDivision.objects.order_by("-date")[:10]

        latest = sorted(
            [x for x in commons] + [x for x in lords],
            key=lambda d: d.date,
            reverse=True,
        )
        return latest
