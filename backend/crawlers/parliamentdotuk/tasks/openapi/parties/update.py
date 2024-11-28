from crawlers.parliamentdotuk.tasks.openapi.parties import schema
from repository.models import Party
from repository.models.party import PartyTheme


def update_party(data: schema.Party, update: bool = False) -> Party:
    get_func = Party.objects.update_or_create if update else Party.objects.get_or_create
    party, created = get_func(
        parliamentdotuk=data.parliamentdotuk,
        defaults={
            "name": data.name,
        },
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
