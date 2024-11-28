from crawlers.parliamentdotuk.tasks.openapi.parties import schema
from repository.models import Party
from repository.models.party import PartyTheme


def update_party(data: schema.Party, update: bool = False) -> Party:
    party, created = Party.objects.resolve(
        parliamentdotuk=data.parliamentdotuk, name=data.name, update=update
    )

    if not created:
        return party

    if (background := data.background_color) and (foreground := data.foreground_color):
        PartyTheme.objects.get_or_create(
            party=party,
            defaults={
                "primary": background,
                "on_primary": foreground,
            },
        )

    return party
