import datetime

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


def create_sample_constituency(
    name: str = "Aberdeen North",
    parliamentdotuk: int = 143469,
    start: datetime.date = datetime.date(1918, 12, 14),
    end: datetime.date = datetime.date(1950, 2, 23),
) -> Constituency:
    return Constituency.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk,
        start=start,
        end=end,
    )


def create_sample_election(
    name: str = "3001 General Election",
    parliamentdotuk: int = 2154,
    date: datetime.date = datetime.date(3001, 5, 15),
    type: str = "General Election",
) -> Election:
    election_type, _ = ElectionType.objects.get_or_create(name=type)

    return Election.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk,
        election_type=election_type,
        date=date,
    )


def create_constituency_result(
    constituency: Constituency,
    election: Election,
    mp: Person,
) -> ConstituencyResult:
    return ConstituencyResult.objects.create(
        constituency=constituency,
        election=election,
        mp=mp,
    )


def create_constituency_result_detail(
    constituency: Constituency,
    election: Election,
    mp: Person,
    parliamentdotuk: int = 4385,
    electorate: int = 1009,
    turnout: int = 600,
    majority: int = 199,
    result: str = "Party hold",
) -> ConstituencyResultDetail:
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
    name: str = "Labour",
    parliamentdotuk: int = 15,
    homepage: str = "https://labour.org.uk/",
    wikipedia: str = "Labour_Party_(UK)",
    short_name: str = "Lab",
    long_name: str = "Labour Party",
    year_founded: int = 1900,
) -> Party:
    return Party.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk,
        homepage=homepage,
        wikipedia=wikipedia,
        long_name=long_name,
        short_name=short_name,
        year_founded=year_founded,
    )


def create_sample_session(
    name: str = "2017-2019",
    parliamentdotuk: int = 730830,
    start: datetime.date = None,
    end: datetime.date = None,
) -> ParliamentarySession:
    return ParliamentarySession.objects.create(
        name=name,
        parliamentdotuk=parliamentdotuk,
        start=start,
        end=end,
    )


def create_sample_commons_division(
    parliamentdotuk: int = 229684,
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
    if callable(session):
        session = session()

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
    parliamentdotuk: int = 724691,
    title: str = "Education (Student Fees, Awards and Support) (Amendment) Regulations 2017",
    date: datetime.date = datetime.date.fromisoformat("2017-04-27"),
    ayes: int = 121,
    noes: int = 159,
    description: str = "<p>Lord Clark of Windermere moved that this House regrets that the Education (Student Fees, Awards and Support) (Amendment) Regulations 2017, which pave the way for students of nursing, midwifery and allied health professionals to receive loans rather than bursaries, have already been seen to discourage degree applications by a quarter, at the same time as Brexit has already reduced European Union migrant nursing and midwifery registrations by over 90 per cent; and that these factors risk turning an increasing problem in the National Health Service into a chronic one that potentially puts at risk safe levels of staffing (SI 2017/114). The House divided:</p>",
    whipped_vote: bool = True,
    division_number: int = 1,
    session: ParliamentarySession = create_sample_session,
) -> LordsDivision:
    if callable(session):
        session = session()

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
    return BillType.objects.create(
        name=name,
        description=description,
    )


def create_sample_bill(
    title: str = "Defibrillators (Availability) Bill",
    parliamentdotuk: int = 1030151,
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
    if callable(bill_type):
        bill_type = bill_type()

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
