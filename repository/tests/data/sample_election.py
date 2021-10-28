import dataclasses
import datetime
import random
from dataclasses import dataclass


@dataclass
class SampleElection:
    pk: int
    name: str
    date: datetime.date


def any_sample_election():
    """Return a copy of a random SampleElection."""
    return dataclasses.replace(random.choice(SAMPLE_ELECTIONS))


SAMPLE_ELECTIONS = [
    SampleElection(397, "2019 General Election", datetime.date(2019, 12, 12)),
    SampleElection(377, "2017 General Election", datetime.date(2017, 6, 8)),
    SampleElection(369, "2015 General Election", datetime.date(2015, 5, 7)),
    SampleElection(19, "2010 General Election", datetime.date(2010, 5, 6)),
    SampleElection(17, "2005 General Election", datetime.date(2005, 5, 5)),
    SampleElection(16, "2001 General Election", datetime.date(2001, 6, 7)),
    SampleElection(15, "1997 General Election", datetime.date(1997, 5, 1)),
    SampleElection(14, "1992 General Election", datetime.date(1992, 4, 9)),
    SampleElection(13, "1987 General Election", datetime.date(1987, 6, 11)),
    SampleElection(12, "1983 General Election", datetime.date(1983, 6, 9)),
    SampleElection(11, "1979 General Election", datetime.date(1979, 5, 3)),
    SampleElection(10, "1974 (Oct) General Election", datetime.date(1974, 10, 10)),
    SampleElection(9, "1974 (Feb) General Election", datetime.date(1974, 2, 28)),
    SampleElection(8, "1970 General Election", datetime.date(1970, 6, 18)),
    SampleElection(5, "1959 General Election", datetime.date(1959, 10, 8)),
    SampleElection(7, "1966 General Election", datetime.date(1966, 3, 31)),
    SampleElection(6, "1964 General Election", datetime.date(1964, 10, 15)),
]
