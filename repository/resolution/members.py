from typing import Optional

from django.db.models import Q, QuerySet

from repository.models.houses import HOUSE_OF_COMMONS, HOUSE_OF_LORDS
from repository.models import Constituency, Election, Person, Party


def get_active_members(**kwargs) -> QuerySet[Person]:
    return Person.objects.filter(active=True, **kwargs)


def get_active_mps(**kwargs) -> QuerySet[Person]:
    return get_active_members(house__name=HOUSE_OF_COMMONS, **kwargs)


def get_active_lords(**kwargs) -> QuerySet[Person]:
    return get_active_members(house__name=HOUSE_OF_LORDS, **kwargs)


def get_active_party_members(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_members(party=party, **kwargs)


def get_party_mps(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_party_members(party=party, house__name=HOUSE_OF_COMMONS, **kwargs)


def get_party_lords(party: Party, **kwargs) -> QuerySet[Person]:
    return get_active_party_members(party=party, house__name=HOUSE_OF_LORDS, **kwargs)


def get_member_by_name(name: str) -> Optional[Person]:
    by_name = Person.objects.filter(
        Q(name__iexact=name) | Q(personalsoknownas__alias__iexact=name),
    )

    if by_name.count() == 1:
        return by_name.first()


def get_member_for_election_result(
    name: str,
    constituency: Constituency,
    election: Election,
) -> Optional[Person]:
    by_name = Person.objects.filter(
        Q(name__iexact=name) | Q(personalsoknownas__alias__iexact=name),
    )

    if by_name.count() == 1:
        return by_name.first()

    by_constituency = by_name.filter(
        Q(constituency=constituency)
        | (
            Q(contestedelection__constituency=constituency)
            & Q(contestedelection__election=election)
        )
    )

    if by_constituency.count() == 1:
        return by_constituency.first()
