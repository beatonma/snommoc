import datetime
import random
from typing import Optional

from repository.models import (
    Bill,
    BillType,
    CommonsDivision,
    Constituency,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
    ElectionType,
    LordsDivision,
    ParliamentarySession,
    Party,
    Person,
)
from repository.tests.data.sample_constituencies import (
    SAMPLE_CONSTITUENCIES,
    any_sample_constituency,
)
from repository.tests.data.sample_election import SAMPLE_ELECTIONS, any_sample_election
from repository.tests.data.sample_members import any_sample_member
from repository.tests.data.sample_parties import SAMPLE_PARTIES, any_sample_party


def _any_int(max: int = 100) -> int:
    return random.randint(1, max)


def _any_id() -> int:
    return _any_int(10_000)


def create_sample_person(
    parliamentdotuk: Optional[int] = None,
    name: Optional[str] = None,
    active: bool = True,
    randomise: bool = True,
    **kwargs,
) -> Person:
    m = any_sample_member()

    if parliamentdotuk:
        m.pk = parliamentdotuk
    elif randomise:
        m.pk = _any_id()

    if name:
        m.name = name

    return Person.objects.create(
        parliamentdotuk=m.pk,
        name=m.name,
        active=active,
        **kwargs,
    )


def create_sample_constituency(
    name: Optional[str] = None,
    parliamentdotuk: Optional[int] = None,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    randomise: bool = True,
) -> Constituency:
    c = any_sample_constituency()

    if name:
        c.name = name

    if parliamentdotuk:
        c.pk = parliamentdotuk
    elif randomise:
        c.pk = _any_id()

    if start:
        c.start = start

    if end:
        c.end = end

    return Constituency.objects.create(
        name=c.name,
        pk=c.pk,
        start=c.start,
        end=c.end,
    )


def create_sample_constituencies():
    """Create Constituencies from sample data."""
    for constituency in SAMPLE_CONSTITUENCIES:
        Constituency.objects.create(
            name=constituency.name,
            pk=constituency.pk,
            start=constituency.start,
            end=constituency.end,
        )


def create_sample_election(
    name: Optional[str] = None,
    parliamentdotuk: Optional[int] = None,
    date: Optional[datetime.date] = None,
    type: str = "General Election",
    randomise: bool = True,
) -> Election:
    """Create an Election with custom data."""
    election_type, _ = ElectionType.objects.get_or_create(name=type)

    e = any_sample_election()

    if name:
        e.name = name

    if parliamentdotuk:
        e.pk = parliamentdotuk
    elif randomise:
        e.pk = _any_id()

    if date:
        e.date = date

    return Election.objects.create(
        name=e.name,
        parliamentdotuk=e.pk,
        date=e.date,
        election_type=election_type,
    )


def create_sample_elections():
    election_type, _ = ElectionType.objects.get_or_create(name="General Election")
    for election in SAMPLE_ELECTIONS:
        Election.objects.create(
            name=election.name,
            parliamentdotuk=election.pk,
            date=election.date,
            election_type=election_type,
        )


def create_constituency_result(
    constituency: Constituency,
    election: Election,
    mp: Person,
) -> ConstituencyResult:
    """Create a ConstituencyResult with custom data."""
    return ConstituencyResult.objects.create(
        constituency=constituency,
        election=election,
        mp=mp,
    )


def create_constituency_result_detail(
    constituency: Constituency,
    election: Election,
    mp: Person,
    parliamentdotuk: Optional[int] = None,
    electorate: Optional[int] = None,
    turnout: Optional[int] = None,
    majority: Optional[int] = None,
    result: str = "Party hold",
) -> ConstituencyResultDetail:
    """Create a ConstituencyResultDetail with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not electorate:
        electorate = _any_int(10_000)

    if not turnout:
        turnout = _any_int(electorate)

    if not majority:
        majority = _any_int(turnout)

    assert turnout <= electorate
    assert majority <= turnout

    constituency_result = create_constituency_result(constituency, election, mp)

    return ConstituencyResultDetail.objects.create(
        parliamentdotuk=parliamentdotuk,
        constituency_result=constituency_result,
        electorate=electorate,
        turnout=turnout,
        turnout_fraction=turnout / electorate,
        majority=majority,
        result=result,
    )


def create_sample_party(
    name: Optional[str] = None,
    parliamentdotuk: Optional[int] = None,
    homepage: Optional[str] = None,
    wikipedia: Optional[str] = None,
    year_founded: int = 0,
    randomise: bool = True,
) -> Party:
    """Create a Party with custom data."""
    party = any_sample_party()

    if name:
        party.name = name

    if parliamentdotuk:
        party.pk = parliamentdotuk
    elif randomise:
        party.pk = _any_id()

    return Party.objects.create(
        name=party.name,
        parliamentdotuk=party.pk,
        homepage=homepage,
        wikipedia=wikipedia,
        year_founded=year_founded,
    )


def create_sample_parties():
    for x in SAMPLE_PARTIES:
        Party.objects.create(parliamentdotuk=x.pk, name=x.name)


def create_sample_session(
    name: str = "2017-2019",
    parliamentdotuk: Optional[int] = None,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
) -> ParliamentarySession:
    """Create a ParliamentarySession with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    return ParliamentarySession.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk,
        start=start,
        end=end,
    )


def create_sample_commons_division(
    parliamentdotuk: Optional[int] = None,
    title: str = "Statutory Instruments: Motion for Approval. That the draft Infrastructure Planning (Radioactive Waste Geological Disposal Facilities) Order 2015, which was laid before this House on 12 January, be approved. Q acc agreed to.",
    abstentions: int = 1,
    ayes: int = 202,
    noes: int = 225,
    did_not_vote: int = 216,
    non_eligible: int = 0,
    errors: int = 0,
    suspended_or_expelled: int = 0,
    date: datetime.date = datetime.date.fromisoformat("2015-03-26"),
    deferred_vote: bool = False,
    session: Optional[ParliamentarySession] = None,
    uin: str = "CD:2015-03-26:188",
    division_number: int = 188,
) -> CommonsDivision:
    """Create a CommonsDivision with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not session:
        session = create_sample_session()

    return CommonsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=title,
        abstentions=abstentions,
        ayes=ayes,
        noes=noes,
        did_not_vote=did_not_vote,
        non_eligible=non_eligible,
        errors=errors,
        suspended_or_expelled=suspended_or_expelled,
        date=date,
        deferred_vote=deferred_vote,
        session=session,
        uin=uin,
        division_number=division_number,
    )


def create_sample_lords_division(
    parliamentdotuk: Optional[int] = None,
    title: str = "Education (Student Fees, Awards and Support) (Amendment) Regulations 2017",
    date: datetime.date = datetime.date.fromisoformat("2017-04-27"),
    ayes: int = 121,
    noes: int = 159,
    description: str = "<p>Lord Clark of Windermere moved that this House regrets that the Education (Student Fees, Awards and Support) (Amendment) Regulations 2017, which pave the way for students of nursing, midwifery and allied health professionals to receive loans rather than bursaries, have already been seen to discourage degree applications by a quarter, at the same time as Brexit has already reduced European Union migrant nursing and midwifery registrations by over 90 per cent; and that these factors risk turning an increasing problem in the National Health Service into a chronic one that potentially puts at risk safe levels of staffing (SI 2017/114). The House divided:</p>",
    whipped_vote: bool = True,
    division_number: int = 1,
    session: Optional[ParliamentarySession] = None,
) -> LordsDivision:
    """Create a LordsDivision with custom data."""

    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not session:
        session = create_sample_session()

    return LordsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=title,
        date=date,
        ayes=ayes,
        noes=noes,
        description=description,
        whipped_vote=whipped_vote,
        session=session,
        division_number=division_number,
    )


def create_sample_bill_type(
    name: str = "Ten Minute Rule",
    description: str = "Private Members' Bill (under the Ten Minute Rule)",
) -> BillType:
    """Create a BillType with custom data."""
    return BillType.objects.create(
        name=name,
        description=description,
    )


def create_sample_bill(
    title: str = "Defibrillators (Availability) Bill",
    parliamentdotuk: Optional[int] = None,
    description: str = "A Bill to require the provision of defibrillators in education establishments, and in leisure, sports and certain other public facilities; to make provision for training persons to operate defibrillators; to make provision for funding the acquisition, installation, use and maintenance of defibrillators; and for connected purposes.",
    act_name: str = "",
    label: str = "Defibrillators (Availability)",
    homepage: str = "http://services.parliament.uk/bills/2017-19/defibrillatorsavailability.html",
    date: datetime.date = datetime.date.fromisoformat("2018-12-20"),
    ballot_number: int = 0,
    bill_chapter: str = "",
    is_private: bool = False,
    is_money_bill: bool = False,
    public_involvement_allowed: bool = False,
    bill_type: Optional[BillType] = None,
    session: Optional[ParliamentarySession] = None,
) -> Bill:
    """Create a Bill with custom data."""

    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not session:
        session = create_sample_session()

    if not bill_type:
        bill_type = create_sample_bill_type()

    return Bill.objects.create(
        title=title,
        parliamentdotuk=parliamentdotuk,
        description=description,
        act_name=act_name,
        label=label,
        homepage=homepage,
        date=date,
        ballot_number=ballot_number,
        bill_chapter=bill_chapter,
        is_private=is_private,
        is_money_bill=is_money_bill,
        public_involvement_allowed=public_involvement_allowed,
        bill_type=bill_type,
        session=session,
    )


def create_sample_constituency_candidate(
    name: Optional[str] = None,
    constituency_result_detail: Optional[ConstituencyResultDetail] = None,
    party_name: Optional[str] = None,
    order: Optional[int] = None,
    votes: Optional[int] = None,
    party: Optional[Party] = any_sample_party(),
) -> ConstituencyCandidate:
    if not constituency_result_detail:
        constituency_result_detail = create_constituency_result_detail(
            constituency=create_sample_constituency(),
            election=create_sample_election(),
            mp=create_sample_person(),
        )

    if not name:
        name = any_sample_member().name

    if not order:
        order = _any_int(10)

    if not votes:
        votes = _any_int(100)

    if not party_name:
        party = any_sample_party()
        party_name = party.name

    return ConstituencyCandidate.objects.create(
        election_result=constituency_result_detail,
        name=name,
        votes=votes,
        order=order,
        party_name=party_name,
        party=party,
    )
