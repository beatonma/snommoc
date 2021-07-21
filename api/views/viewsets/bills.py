from django.db.models import Q

from api.serializers.bills import (
    BillSerializer,
    InlineBillSerializer,
)
from api.views.viewsets import KeyRequiredViewSet
from repository.models import Bill
from surface.models import FeaturedBill
from util.cleanup import UnusedClass
from util.time import get_today


class BillViewSet(KeyRequiredViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class RecentlyUpdatedBillsViewSet(KeyRequiredViewSet):
    serializer_class = InlineBillSerializer

    def get_queryset(self):
        return Bill.objects.order_by("date")[:10]


class _FeaturedBillsViewSet(UnusedClass, KeyRequiredViewSet):
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
