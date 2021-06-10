"""

"""
import logging

from django.db.models import Q

from api.serializers.motd import MessageOfTheDaySerializer
from api.views.viewsets import KeyRequiredViewSet
from surface.models import MessageOfTheDay
from util.time import get_today

log = logging.getLogger(__name__)


class MessageOfTheDayViewSet(KeyRequiredViewSet):
    serializer_class = MessageOfTheDaySerializer

    def get_queryset(self):
        today = get_today()
        return MessageOfTheDay.objects.filter(
            Q(display=True)
            & (Q(start__isnull=True) | Q(start__lte=today))
            & (Q(end__isnull=True) | Q(end__gte=today))
        )
