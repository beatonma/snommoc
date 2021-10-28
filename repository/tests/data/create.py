import datetime
import random

from repository.models import (
    Bill,
    BillType,
    CommonsDivision,
    Constituency,
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


def _any_id() -> int:
    return random.randint(1, 9999)


def create_sample_person(
    parliamentdotuk: int = None,
    name: str = None,
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
    name: str = None,
    parliamentdotuk: int = None,
    start: datetime.date = None,
    end: datetime.date = None,
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
    name: str = None,
    parliamentdotuk: int = None,
    date: datetime.date = None,
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
    parliamentdotuk: int = _any_id,
    electorate: int = 1009,
    turnout: int = 600,
    majority: int = 199,
    result: str = "Party hold",
) -> ConstituencyResultDetail:
    """Create a ConstituencyResultDetail with custom data."""
    constituency_result = create_constituency_result(constituency, election, mp)

    return ConstituencyResultDetail.objects.create(
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
        constituency_result=constituency_result,
        electorate=electorate,
        turnout=turnout,
        turnout_fraction=turnout / electorate,
        majority=majority,
        result=result,
    )


def create_sample_party(
    name: str = "Labour",
    parliamentdotuk: int = _any_id,
    homepage: str = "https://labour.org.uk/",
    wikipedia: str = "Labour_Party_(UK)",
    short_name: str = "Lab",
    long_name: str = "Labour Party",
    year_founded: int = 1900,
) -> Party:
    """Create a Party with custom data."""
    return Party.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
        homepage=homepage,
        wikipedia=wikipedia,
        long_name=long_name,
        short_name=short_name,
        year_founded=year_founded,
    )


def create_sample_session(
    name: str = "2017-2019",
    parliamentdotuk: int = _any_id,
    start: datetime.date = None,
    end: datetime.date = None,
) -> ParliamentarySession:
    """Create a ParliamentarySession with custom data."""
    return ParliamentarySession.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
        start=start,
        end=end,
    )


def create_sample_commons_division(
    parliamentdotuk: int = _any_id,
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
    session: ParliamentarySession = create_sample_session,
    uin: str = "CD:2015-03-26:188",
    division_number: int = 188,
) -> CommonsDivision:
    """Create a CommonsDivision with custom data."""
    if callable(session):
        session = session()

    return CommonsDivision.objects.create(
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
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
    parliamentdotuk: int = _any_id,
    title: str = "Education (Student Fees, Awards and Support) (Amendment) Regulations 2017",
    date: datetime.date = datetime.date.fromisoformat("2017-04-27"),
    ayes: int = 121,
    noes: int = 159,
    description: str = "<p>Lord Clark of Windermere moved that this House regrets that the Education (Student Fees, Awards and Support) (Amendment) Regulations 2017, which pave the way for students of nursing, midwifery and allied health professionals to receive loans rather than bursaries, have already been seen to discourage degree applications by a quarter, at the same time as Brexit has already reduced European Union migrant nursing and midwifery registrations by over 90 per cent; and that these factors risk turning an increasing problem in the National Health Service into a chronic one that potentially puts at risk safe levels of staffing (SI 2017/114). The House divided:</p>",
    whipped_vote: bool = True,
    division_number: int = 1,
    session: ParliamentarySession = create_sample_session,
) -> LordsDivision:
    """Create a LordsDivision with custom data."""
    return LordsDivision.objects.create(
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
        title=title,
        date=date,
        ayes=ayes,
        noes=noes,
        description=description,
        whipped_vote=whipped_vote,
        session=session() if callable(session) else session,
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
    parliamentdotuk: int = _any_id,
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
    bill_type: BillType = create_sample_bill_type,
    session: ParliamentarySession = None,
) -> Bill:
    """Create a Bill with custom data."""
    return Bill.objects.create(
        title=title,
        parliamentdotuk=parliamentdotuk()
        if callable(parliamentdotuk)
        else parliamentdotuk,
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
        bill_type=bill_type() if callable(bill_type) else bill_type,
        session=session,
    )
