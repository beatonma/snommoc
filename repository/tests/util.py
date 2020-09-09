"""

"""

import logging

from repository.models import Person

log = logging.getLogger(__name__)


def create_sample_person(
        parliamentdotuk: int = 1423,
        name: str = 'Boris Johnson',
        active: bool = True,
        **kwargs
) -> Person:
    person = Person.objects.create(
        parliamentdotuk=parliamentdotuk,
        name=name,
        active=active,
        **kwargs
    )
    person.save()
    return person
