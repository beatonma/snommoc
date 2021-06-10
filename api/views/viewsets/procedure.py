"""
Viewsets for any data about Parliamentary procedure - bills, divisions, votes, etc.
"""
import logging

from django.db.models import Q

from api.serializers import (
    CommonsDivisionSerializer,
    LordsDivisionSerializer,
)
from api.serializers.bills import BillSerializer
from api.serializers.inline import InlineBillSerializer
from api.serializers.votes import (
    GenericInlineDivisionSerializer,
)
from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivision,
)
from surface.models import (
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
)
from util.time import get_today

log = logging.getLogger(__name__)


class BillViewSet(KeyRequiredViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class FeaturedBillsViewSet(KeyRequiredViewSet):
    """Return a list of 'featured' bills."""

    serializer_class = InlineBillSerializer

    def get_queryset(self):
        today = get_today()
        qs = (
            FeaturedBill.objects.filter(Q(start__isnull=True) | Q(start__lte=today))
            .filter(Q(end__isnull=True) | Q(end__gte=today))
            .select_related("target")
        )
        return [item.target for item in qs]


class RecentlyUpdatedBillsViewSet(KeyRequiredViewSet):
    serializer_class = InlineBillSerializer

    def get_queryset(self):
        return Bill.objects.order_by("date")[:10]


class FeaturedDivisionsViewSet(KeyRequiredViewSet):
    """Return a list of 'featured' divisions - lords and commons combined.."""

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


class CommonsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Commons division, including vote results.."""

    queryset = CommonsDivision.objects.all()

    serializer_class = CommonsDivisionSerializer


class LordsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Lords division, including vote results.."""

    queryset = LordsDivision.objects.all()

    serializer_class = LordsDivisionSerializer
