"""
Viewsets for any data about Parliamentary procedure - bills, divisions, votes, etc.
"""
import datetime
import logging

from django.db.models import Q

from api.serializers import (
    CommonsDivisionSerializer,
    LordsDivisionSerializer,
)
from api.serializers.bills import BillSerializer
from api.serializers.inline import InlineBillSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivision,
)
from surface.models import FeaturedBill

log = logging.getLogger(__name__)


class BillViewSet(KeyRequiredViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class FeaturedBillsViewSet(KeyRequiredViewSet):
    """Return a list of 'featured' bills."""
    serializer_class = InlineBillSerializer

    def get_queryset(self):
        today = datetime.date.today()
        qs = FeaturedBill.objects.filter(
            Q(start__isnull=True) | Q(start__lte=today)
        ).filter(
            Q(end__isnull=True) | Q(end__gte=today)
        ).select_related('bill')
        return [item.bill for item in qs]


class CommonsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Commons division, including vote results.."""
    queryset = CommonsDivision.objects.all()

    serializer_class = CommonsDivisionSerializer


class LordsDivisionViewSet(KeyRequiredViewSet):
    """Return information about a Lords division, including vote results.."""
    queryset = LordsDivision.objects.all()

    serializer_class = LordsDivisionSerializer
