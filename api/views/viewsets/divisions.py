from django.db.models import Q

from api.serializers.divisions import CommonsDivisionSerializer, LordsDivisionSerializer
from api.serializers.divisions.votes import GenericInlineDivisionSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import CommonsDivision, LordsDivision
from surface.models import FeaturedCommonsDivision, FeaturedLordsDivision
from util.cleanup import UnusedClass
from util.time import get_today


class CommonsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Commons division, including vote results.."""

    queryset = CommonsDivision.objects.all()
    serializer_class = CommonsDivisionSerializer


class LordsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Lords division, including vote results.."""

    queryset = LordsDivision.objects.all()
    serializer_class = LordsDivisionSerializer


class _FeaturedDivisionsViewSet(UnusedClass, KeyRequiredViewSet):
    """Return a list of 'featured' divisions - lords and commons combined."""

    serializer_class = GenericInlineDivisionSerializer

    def get_queryset(self):
        today = get_today()
        filters = (Q(start__isnull=True) | Q(start__lte=today)) & (
            Q(end__isnull=True) | Q(end__gte=today)
        )
        commons = FeaturedCommonsDivision.objects.filter(filters).select_related(
            "target"
        )
        lords = FeaturedLordsDivision.objects.filter(filters).select_related("target")

        return [x.division for x in commons] + [y.division for y in lords]


class RecentlyUpdatedDivisionsViewSet(KeyRequiredViewSet):
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
