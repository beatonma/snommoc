from typing import Optional

from repository.models import Party, PartyAlsoKnownAs


def get_party_by_name(name_stub: str) -> Optional[Party]:
    """Try to resolve the given string (which may be a name, acronym, shorthand) to a Party instance."""
    try:
        return Party.objects.get(name__iexact=name_stub)
    except Party.DoesNotExist:
        pass

    try:
        return PartyAlsoKnownAs.objects.get(alias__iexact=name_stub).canonical
    except PartyAlsoKnownAs.DoesNotExist:
        pass
