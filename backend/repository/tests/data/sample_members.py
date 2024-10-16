from dataclasses import dataclass

from repository.tests.data.sample import any_sample_of
from repository.tests.data.sample_parties import SampleParty


@dataclass
class SampleMember:
    pk: int
    name: str
    party: SampleParty


def any_sample_mp() -> SampleMember:
    """Return a copy of a random SampleMember MP."""
    return any_sample_of(SAMPLE_MPS)


def any_sample_lord() -> SampleMember:
    """Return a copy of a random SampleMember Lord."""
    return any_sample_of(SAMPLE_LORDS)


def any_sample_member() -> SampleMember:
    """Return a copy of a random SampleMember."""
    return any_sample_of(SAMPLE_MEMBERS)


SAMPLE_MPS = [
    SampleMember(4768, "Julie Marson", SampleParty(4, "Conservative")),
    SampleMember(4589, "Robert Courts", SampleParty(4, "Conservative")),
    SampleMember(3913, "Jack Dromey", SampleParty(15, "Labour")),
    SampleMember(4360, "Gavin Robinson", SampleParty(7, "Democratic Unionist Party")),
    SampleMember(223, "Dr Liam Fox", SampleParty(4, "Conservative")),
    SampleMember(4409, "Naz Shah", SampleParty(15, "Labour")),
    SampleMember(3939, "Andrew Percy", SampleParty(4, "Conservative")),
    SampleMember(8, "Mrs Theresa May", SampleParty(4, "Conservative")),
    SampleMember(4792, "Paul Bristow", SampleParty(4, "Conservative")),
    SampleMember(4569, "Jim McMahon", SampleParty(10015, "Labour (Co-op)")),
    SampleMember(4819, "Theo Clarke", SampleParty(4, "Conservative")),
    SampleMember(1565, "Philip Davies", SampleParty(4, "Conservative")),
    SampleMember(4384, "Mike Wood", SampleParty(4, "Conservative")),
    SampleMember(4411, "Lucy Allan", SampleParty(4, "Conservative")),
    SampleMember(4789, "Marco Longhi", SampleParty(4, "Conservative")),
    SampleMember(4857, "Carla Lockhart", SampleParty(7, "Democratic Unionist Party")),
    SampleMember(1396, "Mr Ian Liddell-Grainger", SampleParty(4, "Conservative")),
    SampleMember(4127, "Julie Elliott", SampleParty(15, "Labour")),
    SampleMember(4872, "David Simmonds", SampleParty(4, "Conservative")),
    SampleMember(4783, "Kate Osborne", SampleParty(15, "Labour")),
    SampleMember(4777, "Sarah Owen", SampleParty(15, "Labour")),
    SampleMember(234, "Sir Gary Streeter", SampleParty(4, "Conservative")),
    SampleMember(4438, "Craig Williams", SampleParty(4, "Conservative")),
    SampleMember(140, "Dame Margaret Hodge", SampleParty(15, "Labour")),
    SampleMember(4836, "Ben Everitt", SampleParty(4, "Conservative")),
    SampleMember(4133, "Andrew Bridgen", SampleParty(4, "Conservative")),
    SampleMember(4465, "Ronnie Cowan", SampleParty(29, "Scottish National Party")),
    SampleMember(54, "Dr Julian Lewis", SampleParty(4, "Conservative")),
    SampleMember(4639, "Bim Afolami", SampleParty(4, "Conservative")),
    SampleMember(1601, "Sir Robert Neill", SampleParty(4, "Conservative")),
]

SAMPLE_LORDS = [
    SampleMember(4685, "Baroness Wyld", SampleParty(4, "Conservative")),
    SampleMember(4171, "Lord Black of Brentwood", SampleParty(4, "Conservative")),
    SampleMember(4881, "Baroness Morrissey", SampleParty(4, "Conservative")),
    SampleMember(2205, "Lord Carey of Clifton", SampleParty(6, "Crossbench")),
    SampleMember(489, "Lord Watts", SampleParty(15, "Labour")),
    SampleMember(3813, "Lord Harries of Pentregarth", SampleParty(6, "Crossbench")),
    SampleMember(3898, "Lord Aberdare", SampleParty(6, "Crossbench")),
    SampleMember(2555, "Lord Morgan", SampleParty(15, "Labour")),
    SampleMember(3702, "Lord Young of Norwood Green", SampleParty(15, "Labour")),
    SampleMember(2669, "Lord Harris of Peckham", SampleParty(4, "Conservative")),
    SampleMember(3515, "Viscount Bridgeman", SampleParty(4, "Conservative")),
    SampleMember(494, "Lord Hutton of Furness", SampleParty(15, "Labour")),
    SampleMember(1916, "Lord Newby", SampleParty(17, "Liberal Democrat")),
    SampleMember(4720, "Lord Brownlow of Shurlock Row", SampleParty(4, "Conservative")),
    SampleMember(1479, "Lord Herbert of South Downs", SampleParty(4, "Conservative")),
    SampleMember(4915, "Baroness Black of Strome", SampleParty(6, "Crossbench")),
    SampleMember(
        940, "Lord Rodgers of Quarry Bank", SampleParty(17, "Liberal Democrat")
    ),
    SampleMember(4694, "Lord Houghton of Richmond", SampleParty(6, "Crossbench")),
    SampleMember(
        4906, "Baroness Fraser of Craigmaddie", SampleParty(4, "Conservative")
    ),
    SampleMember(4220, "Lord Dannatt", SampleParty(6, "Crossbench")),
    SampleMember(2518, "Baroness Greengross", SampleParty(6, "Crossbench")),
    SampleMember(2127, "Lord Selsdon", SampleParty(4, "Conservative")),
    SampleMember(
        2439, "Lord Phillips of Worth Matravers", SampleParty(6, "Crossbench")
    ),
    SampleMember(2143, "Lord Rotherwick", SampleParty(4, "Conservative")),
    SampleMember(4247, "Lord Ashton of Hyde", SampleParty(4, "Conservative")),
    SampleMember(4200, "Lord True", SampleParty(4, "Conservative")),
    SampleMember(547, "Lord Wigley", SampleParty(22, "Plaid Cymru")),
    SampleMember(4340, "Lord Cashman", SampleParty(49, "Non-affiliated")),
    SampleMember(2476, "Baroness Prashar", SampleParty(6, "Crossbench")),
    SampleMember(4898, "Lord Udny-Lister", SampleParty(4, "Conservative")),
]

SAMPLE_MEMBERS = SAMPLE_MPS + SAMPLE_LORDS
