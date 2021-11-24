from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from api.serializers.zeitgeist import ZeitgeistSerializer
from api.views.viewsets import KeyRequiredViewSet
from repository.models import (
    Bill,
    CommonsDivision,
    LordsDivisionRedux,
    Person,
)
from surface.models import (
    MessageOfTheDay,
    ZeitgeistItem,
)
from util.time import get_today


class ZeitgeistViewSet(KeyRequiredViewSet):
    """
    Trending/featured stuff.
    """

    def get_queryset(self):
        return ZeitgeistItem.objects.all()

    def get_object(self):
        today = get_today()
        items = self.filter_queryset(self.get_queryset())

        people = items.filter(target_type=ContentType.objects.get_for_model(Person))
        commons_divisions = items.filter(
            target_type=ContentType.objects.get_for_model(CommonsDivision)
        )
        lords_divisions = items.filter(
            target_type=ContentType.objects.get_for_model(LordsDivisionRedux)
        )
        bills = items.filter(target_type=ContentType.objects.get_for_model(Bill))

        motd = MessageOfTheDay.objects.filter(
            Q(display=True)
            & (Q(start__isnull=True) | Q(start__lte=today))
            & (Q(end__isnull=True) | Q(end__gte=today))
        )

        return {
            "motd": motd,
            "people": people,
            "divisions": commons_divisions.union(lords_divisions),
            "bills": bills,
        }

    serializer_class = ZeitgeistSerializer
