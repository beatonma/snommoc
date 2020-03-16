"""
Viewsets for any data about Parliamentary procedure - bills, divisions, votes, etc.
"""
import datetime
import logging

from django.db.models import Q

from api.serializers.inline import InlineBillSerializer
from api.views.viewsets import KeyRequiredViewSet
from surface.models import FeaturedBill

log = logging.getLogger(__name__)


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
