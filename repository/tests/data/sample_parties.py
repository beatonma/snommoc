from dataclasses import dataclass

from repository.tests.data.sample import any_sample_of


@dataclass
class SampleParty:
    pk: int
    name: str


def any_sample_party() -> SampleParty:
    return any_sample_of(SAMPLE_PARTIES)


SAMPLE_PARTIES = [
    SampleParty(15, "Labour"),
    SampleParty(30, "Sinn Féin"),
    SampleParty(4, "Conservative"),
    SampleParty(29, "Scottish National Party"),
    SampleParty(17, "Liberal Democrat"),
    SampleParty(6, "Crossbench"),
    SampleParty(49, "Non-affiliated"),
    SampleParty(8, "Independent"),
    SampleParty(7, "Democratic Unionist Party"),
    SampleParty(12, "Independent SDP"),
    SampleParty(38, "Ulster Unionist Party"),
    SampleParty(47, "Speaker"),
    SampleParty(32, "Social Democratic Party"),
    SampleParty(10, "Independent Labour"),
    SampleParty(9, "Independent Conservative"),
    SampleParty(2, "Anti H Block"),
    SampleParty(1004, "The Independent Group for Change"),
    SampleParty(21, "Other"),
    SampleParty(22, "Plaid Cymru"),
    SampleParty(16, "Liberal"),
    SampleParty(20, "Opposition Unity"),
    SampleParty(41, "United Ulster Unionist Party"),
    SampleParty(31, "Social Democratic & Labour Party"),
    SampleParty(1, "Alliance"),
    SampleParty(13, "Independent Socialist"),
    SampleParty(283, "Lord Speaker"),
    SampleParty(26, "Respect"),
    SampleParty(24, "Referendum"),
    SampleParty(19, "National Liberal & Conservative"),
    SampleParty(36, "Ulster Popular Unionist Party"),
    SampleParty(44, "Green Party"),
    SampleParty(39, "United Kingdom Unionist"),
    SampleParty(52, "Independent Ulster Unionist"),
    SampleParty(53, "Independent Social Democrat"),
    SampleParty(35, "UK Independence Party"),
    SampleParty(10015, "Labour (Co-op)"),
    SampleParty(1034, "Alba Party"),
    SampleParty(43, "Labour Independent"),
    SampleParty(14, "Independent Unionist"),
    SampleParty(3, "Bishops"),
    SampleParty(5, "Conservative Independent"),
]
