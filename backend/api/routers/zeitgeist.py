from datetime import timedelta

from api.cache import cache_view
from api.schema.zeitgeist import ZeitgeistSchema
from django.http import HttpRequest
from ninja import Router
from repository.models import Bill, CommonsDivision, LordsDivision, Person
from surface.models import MessageOfTheDay, ZeitgeistItem
from util.time import get_today

router = Router(tags=["Zeitgeist"])


@router.get("/", response=ZeitgeistSchema)
@cache_view(timeout=timedelta(hours=6).total_seconds(), cache_key="zeitgeist")
def zeitgeist(request: HttpRequest):
    today = get_today()
    items = ZeitgeistItem.objects.all()

    people = items.for_target_type(Person)
    commons_divisions = items.for_target_type(CommonsDivision)
    lords_divisions = items.for_target_type(LordsDivision)
    bills = items.for_target_type(Bill)

    motd = MessageOfTheDay.objects.filter_date(today)

    return {
        "motd": motd,
        "people": people,
        "divisions": commons_divisions.union(lords_divisions),
        "bills": bills,
    }
