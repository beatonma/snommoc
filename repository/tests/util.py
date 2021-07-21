from repository.models import Person


def create_sample_person(
    parliamentdotuk: int = 1423,
    name: str = "Boris Johnson",
    active: bool = True,
    **kwargs,
) -> Person:
    return Person.objects.create(
        parliamentdotuk=parliamentdotuk,
        name=name,
        active=active,
        **kwargs,
    )
