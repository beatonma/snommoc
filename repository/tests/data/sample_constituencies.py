from dataclasses import dataclass
from datetime import date
from typing import Optional

from repository.tests.data.sample import any_sample_of


@dataclass
class SampleConstituency:
    name: str
    pk: int
    start: date
    end: Optional[date]


def any_sample_constituency():
    """Return a copy of a random SampleConstituency."""
    return any_sample_of(SAMPLE_CONSTITUENCIES)


SAMPLE_CONSTITUENCIES = [
    SampleConstituency(
        "Aberdeen Central",
        143468,
        date(1997, 5, 1),
        date(2005, 5, 5),
    ),
    SampleConstituency(
        "Aberdeen North",
        143469,
        date(1918, 12, 14),
        date(1950, 2, 23),
    ),
    SampleConstituency(
        "Aberdeen North",
        143470,
        date(1950, 2, 23),
        date(1974, 2, 28),
    ),
    SampleConstituency(
        "Aberdeen North",
        143471,
        date(1974, 2, 28),
        date(1983, 6, 9),
    ),
    SampleConstituency(
        "Aberdeen North",
        143472,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Aberdeen North",
        143473,
        date(1997, 5, 1),
        date(2005, 5, 5),
    ),
    SampleConstituency(
        "Aberdeen North",
        143474,
        date(2005, 4, 5),
        None,
    ),
    SampleConstituency(
        "Aberdeen South",
        143475,
        date(1918, 12, 14),
        date(1950, 2, 23),
    ),
    SampleConstituency(
        "Aberdeen South",
        143476,
        date(1950, 2, 23),
        date(1974, 2, 28),
    ),
    SampleConstituency(
        "Aberdeen South",
        143477,
        date(1974, 2, 28),
        date(1983, 6, 9),
    ),
    SampleConstituency(
        "Inverness",
        145016,
        date(1918, 12, 14),
        date(1950, 2, 23),
    ),
    SampleConstituency(
        "Inverness",
        145017,
        date(1950, 2, 23),
        date(1974, 2, 28),
    ),
    SampleConstituency(
        "Inverness",
        145018,
        date(1974, 2, 28),
        date(1983, 6, 9),
    ),
    SampleConstituency(
        "Inverness East, Nairn & Lochaber",
        145019,
        date(1997, 5, 1),
        date(2005, 5, 5),
    ),
    SampleConstituency(
        "Inverness, Nairn & Lochaber",
        145020,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Inverness, Nairn, Badenoch and Strathspey",
        145021,
        date(2005, 4, 5),
        None,
    ),
    SampleConstituency(
        "Ross, Skye & Inverness West",
        145915,
        date(1997, 5, 1),
        date(2005, 5, 5),
    ),
    SampleConstituency(
        "Barnsley",
        143584,
        date(1918, 12, 14),
        date(1950, 2, 23),
    ),
    SampleConstituency(
        "Barnsley",
        143585,
        date(1950, 2, 23),
        date(1974, 2, 28),
    ),
    SampleConstituency(
        "Barnsley",
        143586,
        date(1974, 2, 28),
        date(1983, 6, 9),
    ),
    SampleConstituency(
        "Barnsley Central",
        143587,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Barnsley Central",
        143588,
        date(1997, 5, 1),
        date(2010, 5, 6),
    ),
    SampleConstituency(
        "Barnsley Central",
        146762,
        date(2010, 5, 6),
        None,
    ),
    SampleConstituency(
        "Barnsley East",
        143589,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Barnsley East",
        146763,
        date(2010, 5, 6),
        None,
    ),
    SampleConstituency(
        "Barnsley East & Mexborough",
        143590,
        date(1997, 5, 1),
        date(2010, 5, 6),
    ),
    SampleConstituency(
        "Barnsley West & Penistone",
        143591,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Barnsley West & Penistone",
        143592,
        date(1997, 5, 1),
        date(2010, 5, 6),
    ),
    SampleConstituency(
        "Dumfriesshire, Clydesdale and Tweeddale",
        144374,
        date(2005, 4, 5),
        None,
    ),
    SampleConstituency(
        "Tweeddale, Ettrick & Lauderdale",
        146426,
        date(1983, 6, 9),
        date(1997, 5, 1),
    ),
    SampleConstituency(
        "Tweeddale, Ettrick & Lauderdale",
        146427,
        date(1997, 5, 1),
        date(2005, 5, 5),
    ),
    SampleConstituency(
        "Ealing, Acton & Shepherd's Bush",
        144408,
        date(1997, 5, 1),
        date(2010, 5, 6),
    ),
]
