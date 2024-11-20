from crawlers.parliamentdotuk.tasks.openapi.parties import schema
from repository.models import Party
from repository.models.party import PartyTheme


def update_party(data: schema.Party) -> Party:
    party, _ = Party.objects.update_or_create(
        parliamentdotuk=data.parliamentdotuk,
        create_defaults={
            "name": data.name,
        },
    )

    if (background := data.background_color) and (foreground := data.foreground_color):
        PartyTheme.objects.get_or_create(
            party=party,
            create_defaults={
                "primary": background,
                "on_primary": foreground,
            },
        )

    return party
