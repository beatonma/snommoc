"""

"""

import logging

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils import timezone

from api.serializers.zeitgeist import ZeitgeistSerializer

from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivision,
    Person,
)
from surface.models import (
    MessageOfTheDay,
    ZeitgeistItem,
)

log = logging.getLogger(__name__)


class ZeitgeistViewSet(KeyRequiredViewSet):
    """
    Trending/featured stuff.
    """
    def get_queryset(self):
        return ZeitgeistItem.objects.all()

    def get_object(self):
        today = timezone.datetime.today()
        queryset = self.filter_queryset(self.get_queryset())
        items = queryset

        people = items.filter(target_type=ContentType.objects.get_for_model(Person))
        commons_divisions = items.filter(target_type=ContentType.objects.get_for_model(CommonsDivision))
        lords_divisions = items.filter(target_type=ContentType.objects.get_for_model(LordsDivision))
        bills = items.filter(target_type=ContentType.objects.get_for_model(Bill))

        motd = MessageOfTheDay.objects.filter(
            Q(display=True)
            & (Q(start__isnull=True) | Q(start__lte=today))
            & (Q(end__isnull=True) | Q(end__gte=today))
        )

        return {
            'motd': motd,
            'people': people,
            'divisions': commons_divisions.union(lords_divisions),
            'bills': bills,
        }

    serializer_class = ZeitgeistSerializer
