import datetime
import random
from typing import Optional

from repository.models import (
    CommonsDivision,
    Constituency,
    ConstituencyCandidate,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
    ElectionType,
    House,
    LordsDivision,
    ParliamentarySession,
    Party,
    Person,
)
from repository.models.bill import Bill, BillStageType, BillType, BillTypeCategory
from repository.tests.data.sample_bills import (
    any_sample_bill_stage_type,
    any_sample_bill_type,
)
from repository.tests.data.sample_constituencies import (
    SAMPLE_CONSTITUENCIES,
    any_sample_constituency,
)
from repository.tests.data.sample_divisions import (
    any_division_description,
    any_division_title,
)
from repository.tests.data.sample_election import SAMPLE_ELECTIONS, any_sample_election
from repository.tests.data.sample_members import any_sample_member
from repository.tests.data.sample_parties import SAMPLE_PARTIES, any_sample_party

LOREM_IPSUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu hendrerit nunc,"
    " sed sodales purus. Vivamus pulvinar et diam sit amet iaculis. Integer nec"
    " elementum urna, a facilisis sem. Aenean commodo ac sapien vel rutrum. In eget"
    " quam est. Sed quis convallis tortor, sit amet lobortis urna. Morbi tempor, augue"
    " id lobortis bibendum, nibh nulla vehicula sapien, id venenatis sapien elit vel"
    " augue. Etiam egestas purus diam, sit amet finibus massa venenatis ut. Donec et"
    " lorem est. Morbi lacus leo, malesuada a laoreet a, vehicula vel ex."
)


def _any_int(max: int = 100) -> int:
    return random.randint(1, max)


def _any_id() -> int:
    return _any_int(10_000)


def _any_date() -> datetime.date:
    return datetime.date(
        year=random.randint(1990, 2025),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )


def _any_bool() -> bool:
    return bool(random.getrandbits(1))


def _any_str(max_length: int = 32) -> str:
    return LOREM_IPSUM[random.randint(0, 100) : random.randint(120, 300)][:max_length]


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
    elif randomise:
        e.name = f"{e.name}{_any_int(100)}"

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
    title: str = None,
    abstentions: int = None,
    ayes: int = None,
    noes: int = None,
    did_not_vote: int = None,
    non_eligible: int = None,
    errors: int = None,
    suspended_or_expelled: int = None,
    date: datetime.date = None,
    deferred_vote: bool = _any_bool(),
    session: Optional[ParliamentarySession] = None,
    uin: str = "CD:2015-03-26:188",
    division_number: int = None,
) -> CommonsDivision:
    """Create a CommonsDivision with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not title:
        title = any_division_title()

    if not session:
        session = create_sample_session()

    if not abstentions:
        abstentions = _any_int(300)

    if not ayes:
        ayes = _any_int(350)

    if not noes:
        noes = _any_int(350)

    if not did_not_vote:
        did_not_vote = _any_int(300)

    if not non_eligible:
        non_eligible = _any_int(300)

    if not errors:
        errors = _any_int(30)

    if not suspended_or_expelled:
        suspended_or_expelled = _any_int(30)

    if not date:
        date = _any_date()

    if not division_number:
        division_number = _any_int(200)

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


def _coerce_house(house: Optional[str]) -> House:
    if house is None:
        house, _ = House.objects.get_or_create(name="Commons")

    elif isinstance(house, str):
        house, _ = House.objects.get_or_create(name=house)

    else:
        raise ValueError(f"_coerce_house got unexpected argument '{house}")

    return house


def create_sample_house(name: Optional[str] = None) -> House:
    if name is None:
        name = random.choice(["Commons", "Lords", "Unassigned"])

    house, _ = House.objects.get_or_create(name=name)

    return house


def create_sample_lords_division(
    parliamentdotuk: Optional[int] = None,
    title: str = None,
    date: datetime.date = None,
    ayes: int = 121,
    noes: int = 159,
    description: str = None,
    whipped_vote: bool = None,
    division_number: int = 1,
) -> LordsDivision:
    """Create a LordsDivision with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not title:
        title = any_division_title()

    if not date:
        date = _any_date()

    if not ayes:
        ayes = _any_int(300)

    if not noes:
        noes = _any_int(300)

    if not description:
        description = any_division_description()

    if whipped_vote is None:
        whipped_vote = _any_bool()

    if not division_number:
        division_number = _any_int(50)

    return LordsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=title,
        date=date,
        authoritative_content_count=ayes,
        authoritative_not_content_count=noes,
        amendment_motion_notes=description,
        is_whipped=whipped_vote,
        number=division_number,
        is_government_content=_any_bool(),
        is_government_win=_any_bool(),
        division_had_tellers=_any_bool(),
        division_was_exclusively_remote=_any_bool(),
        is_house=_any_bool(),
        teller_content_count=_any_bool(),
        teller_not_content_count=_any_bool(),
        member_content_count=_any_int(500),
        member_not_content_count=_any_int(500),
    )


def create_sample_bill_stage_type(
    parliamentdotuk: Optional[int] = None,
    name: Optional[str] = None,
    house: Optional[str] = None,
) -> BillStageType:
    sample = any_sample_bill_stage_type()

    if parliamentdotuk:
        sample.id = parliamentdotuk

    if name:
        sample.name = name

    return BillStageType.objects.update_or_create(
        parliamentdotuk=sample.id,
        defaults={
            "name": sample.name,
            "house": _coerce_house(house or sample.house),
        },
    )[0]


def create_sample_bill_type(
    parliamentdotuk: Optional[int] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[BillTypeCategory] = None,
) -> BillType:
    sample = any_sample_bill_type()

    if parliamentdotuk:
        sample.id = parliamentdotuk

    if name:
        sample.name = name

    if description:
        sample.description = description

    if isinstance(category, str):
        category, _ = BillTypeCategory.objects.get_or_create(name=category)

    elif not category:
        category, _ = BillTypeCategory.objects.get_or_create(name=sample.category)

    return BillType.objects.update_or_create(
        parliamentdotuk=sample.id,
        defaults={
            "name": sample.name,
            "description": sample.description,
            "category": category,
        },
    )[0]


def create_sample_bill(
    parliamentdotuk: Optional[int] = None,
    short_title: Optional[str] = None,
    long_title: Optional[str] = None,
    last_update: Optional[datetime.datetime] = None,
    bill_type: Optional[BillType] = None,
) -> Bill:
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not short_title:
        short_title = _any_str()

    if not long_title:
        long_title = _any_str()

    if not last_update:
        last_update = _any_date()

    if not bill_type:
        bill_type = create_sample_bill_type()

    session = create_sample_session()

    bill = Bill.objects.create(
        parliamentdotuk=parliamentdotuk,
        short_title=short_title,
        long_title=long_title,
        summary=_any_str(),
        last_update=last_update,
        date_withdrawn=_any_date(),
        bill_type=bill_type,
        session_introduced=session,
        is_act=_any_bool(),
        is_defeated=_any_bool(),
        current_house=create_sample_house(),
        originating_house=create_sample_house(),
    )
    bill.sessions.set([session])
    return bill


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
    )[0]
