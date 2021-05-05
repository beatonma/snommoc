from datetime import date

from repository.models import Constituency


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
    ),

    Constituency.objects.create(
        name="Barnsley",
        pk=143584,
        start=date(1918, 12, 14),
        end=date(1950, 2, 23),
    )
    Constituency.objects.create(
        name="Barnsley",
        pk=143585,
        start=date(1950, 2, 23),
        end=date(1974, 2, 28),
    )
    Constituency.objects.create(
        name="Barnsley",
        pk=143586,
        start=date(1974, 2, 28),
        end=date(1983, 6, 9),
    )
    Constituency.objects.create(
        name="Barnsley Central",
        pk=143587,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Barnsley Central",
        pk=143588,
        start=date(1997, 5, 1),
        end=date(2010, 5, 6),
    )
    Constituency.objects.create(
        name="Barnsley Central",
        pk=146762,
        start=date(2010, 5, 6),
        end=None,
    )
    Constituency.objects.create(
        name="Barnsley East",
        pk=143589,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Barnsley East",
        pk=146763,
        start=date(2010, 5, 6),
        end=None,
    )
    Constituency.objects.create(
        name="Barnsley East & Mexborough",
        pk=143590,
        start=date(1997, 5, 1),
        end=date(2010, 5, 6),
    )
    Constituency.objects.create(
        name="Barnsley West & Penistone",
        pk=143591,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Barnsley West & Penistone",
        pk=143592,
        start=date(1997, 5, 1),
        end=date(2010, 5, 6),
    )

    Constituency.objects.create(
        name="Dumfriesshire, Clydesdale and Tweeddale",
        pk=144374,
        start=date(2005, 4, 5),
        end=None,
    )
    Constituency.objects.create(
        name="Tweeddale, Ettrick & Lauderdale",
        pk=146426,
        start=date(1983, 6, 9),
        end=date(1997, 5, 1),
    )
    Constituency.objects.create(
        name="Tweeddale, Ettrick & Lauderdale",
        pk=146427,
        start=date(1997, 5, 1),
        end=date(2005, 5, 5),
    )

    Constituency.objects.create(
        name="Ealing, Acton & Shepherd's Bush",
        pk=144408,
        start=date(1997, 5, 1),
        end=date(2010, 5, 6),
    )
