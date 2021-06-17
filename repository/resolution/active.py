from django.db.models import QuerySet

from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models import Constituency, Person, Party


def get_active_members(**kwargs) -> QuerySet[Person]:
    return Person.objects.filter(active=True, **kwargs)


def get_active_mps(**kwargs):
    return get_active_members(house__name=HOUSE_OF_COMMONS, **kwargs)


def get_active_lords(**kwargs):
    return get_active_members(house__name=HOUSE_OF_LORDS, **kwargs)


def get_active_constituencies(**kwargs):
    return Constituency.objects.filter(end__isnull=True, **kwargs)


def get_active_party_members(party: Party, **kwargs):
    return get_active_members(party=party, **kwargs)


def get_party_mps(party: Party, **kwargs):
    return get_active_party_members(party=party, house__name=HOUSE_OF_COMMONS, **kwargs)


def get_party_lords(party: Party, **kwargs):
    return get_active_party_members(party=party, house__name=HOUSE_OF_LORDS, **kwargs)
