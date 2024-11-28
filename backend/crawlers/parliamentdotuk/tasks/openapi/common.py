from repository.models import Party, Person

from .parties.schema import Party as PartySchema
from .parties.update import update_party


def resolve_person(
    person_id: int,
    name: str | None,
    *,
    party: Party | None = None,
    party_schema: PartySchema | None = None,
    party_id: int | None = None,
    party_name: str | None = None,
    defaults: dict | None = None,
) -> Person | None:
    """Get or create a member with commonly available api data.

    A person may be referenced in many API responses, each of which
    varies in the level of detail available. If the person already exists
    in our database we can simply retrieve them by their parliamentdotuk ID.
    Otherwise, create the new instance using as much information is available.

    API references to people usually include an ID, name and party. Other
    values may be passed via defaults."""

    if not person_id:
        return None

    defaults = {**(defaults or {})}

    party = party or _resolve_party(party_schema, party_id, party_name)
    if party:
        defaults["party"] = party

    return Person.objects.resolve(
        parliamentdotuk=person_id,
        name=name,
        defaults=defaults,
    )


def _resolve_party(
    party_schema: PartySchema | None,
    party_id: int | None,
    party_name: str | None,
) -> Party | None:
    if party_schema:
        return update_party(party_schema)

    party, _ = Party.objects.resolve(parliamentdotuk=party_id, name=party_name)
    return party
