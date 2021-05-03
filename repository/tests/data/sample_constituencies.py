from repository.models import Constituency
from datetime import date


def create_sample_constituencies():
    Constituency.objects.create(
        name="Aberdeen Central",
        pk=143468,
        start=date(1997, 5, 1),
        end=date(2005, 5, 5),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143469,
        start=date(1918, 12, 14),
        end=date(1950, 2, 23),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143470,
        start=date(1950, 2, 23),
        end=date(1974, 2, 28),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143471,
        start=date(1974, 2, 28),
        end=date(1983, 6, 9),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143472,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143473,
        start=date(1997, 5, 1),
        end=date(2005, 5, 5),
    )
    Constituency.objects.create(
        name="Aberdeen North",
        pk=143474,
        start=date(2005, 4, 5),
        end=None,
    )
    Constituency.objects.create(
        name="Aberdeen South",
        pk=143475,
        start=date(1918, 12, 14),
        end=date(1950, 2, 23),
    )
    Constituency.objects.create(
        name="Aberdeen South",
        pk=143476,
        start=date(1950, 2, 23),
        end=date(1974, 2, 28),
    )
    Constituency.objects.create(
        name="Aberdeen South",
        pk=143477,
        start=date(1974, 2, 28),
        end=date(1983, 6, 9),
    )

    Constituency.objects.create(
        name="Inverness",
        pk=145016,
        start=date(1918, 12, 14),
        end=date(1950, 2, 23),
    )
    Constituency.objects.create(
        name="Inverness",
        pk=145017,
        start=date(1950, 2, 23),
        end=date(1974, 2, 28),
    )
    Constituency.objects.create(
        name="Inverness",
        pk=145018,
        start=date(1974, 2, 28),
        end=date(1983, 6, 9),
    )
    Constituency.objects.create(
        name="Inverness East, Nairn & Lochaber",
        pk=145019,
        start=date(1997, 5, 1),
        end=date(2005, 5, 5),
    )
    Constituency.objects.create(
        name="Inverness, Nairn & Lochaber",
        pk=145020,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Inverness, Nairn, Badenoch and Strathspey",
        pk=145021,
        start=date(2005, 4, 5),
        end=None,
    )
    Constituency.objects.create(
        name="Ross, Skye & Inverness West",
        pk=145915,
        start=date(1997, 5, 1),
        end=date(2005, 5, 5),
    )

    # Constituency.objects.create(
    #     pk=143465,
    #     name="Aberavon",
    # )
    # Constituency.objects.create(
    #     pk=143468,
    #     name="Aberdeen Central",
    # )
    # Constituency.objects.create(
    #     pk=143473,
    #     name="Aberdeen North",
    # )
    # Constituency.objects.create(
    #     pk=145419,
    #     name="Mid Ulster",
    # )
    # Constituency.objects.create(
    #     pk=145460,
    #     name="Montgomeryshire",
    # )
    # Constituency.objects.create(
    #     pk=145463,
    #     name="Moray",
    # )
    # Constituency.objects.create(
    #     pk=145471,
    #     name="Morecambe & Lunesdale",
    # )
    # Constituency.objects.create(
    #     pk=145473,
    #     name="Morley & Rothwell",
    # )
    # Constituency.objects.create(
    #     pk=145521,
    #     name="Newcastle upon Tyne East & Wallsend",
    # )
    # Constituency.objects.create(
    #     pk=145526,
    #     name="Newcastle upon Tyne North",
    # )
    # Constituency.objects.create(
    #     pk=145534,
    #     name="Newcastle-under-Lyme",
    # )
    # Constituency.objects.create(
    #     pk=145545,
    #     name="Newport East",
    # )
    # Constituency.objects.create(
    #     pk=145547,
    #     name="Newport West",
    # )
    # Constituency.objects.create(
    #     pk=145549,
    #     name="Newry & Armagh",
    # )
    # Constituency.objects.create(
    #     pk=145557,
    #     name="Normanton",
    # )
    # Constituency.objects.create(
    #     pk=145563,
    #     name="North Antrim",
    # )
    # Constituency.objects.create(
    #     pk=145571,
    #     name="North Cornwall",
    # )
    # Constituency.objects.create(
    #     pk=145861,
    #     name="Reading West",
    # )
    # Constituency.objects.create(
    #     pk=145864,
    #     name="Redcar",
    # )
    # Constituency.objects.create(
    #     pk=145865,
    #     name="Redditch",
    # )
    # Constituency.objects.create(
    #     pk=145866,
    #     name="Regent's Park & Kensington North",
    # )
    # Constituency.objects.create(
    #     pk=145871,
    #     name="Reigate",
    # )
