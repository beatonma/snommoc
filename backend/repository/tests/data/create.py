import datetime
import random

from repository.models import (
    CommonsDivision,
    Constituency,
    ConstituencyCandidate,
    ConstituencyRepresentative,
    ConstituencyResult,
    ConstituencyResultDetail,
    Election,
    ElectionType,
    House,
    LordsDivision,
    ParliamentarySession,
    Party,
    PartyGenderDemographics,
    Person,
)
from repository.models.bill import Bill, BillStageType, BillType, BillTypeCategory
from repository.models.person import PersonStatus
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
from util.time import tzdatetime

LOREM_IPSUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu hendrerit nunc,"
    " sed sodales purus. Vivamus pulvinar et diam sit amet iaculis. Integer nec"
    " elementum urna, a facilisis sem. Aenean commodo ac sapien vel rutrum. In eget"
    " quam est. Sed quis convallis tortor, sit amet lobortis urna. Morbi tempor, augue"
    " id lobortis bibendum, nibh nulla vehicula sapien, id venenatis sapien elit vel"
    " augue. Etiam egestas purus diam, sit amet finibus massa venenatis ut. Donec et"
    " lorem est. Morbi lacus leo, malesuada a laoreet a, vehicula vel ex."
)


def _any_int(_max: int = 100, _min: int = 0) -> int:
    return random.randint(_min, _max)


def _any_id() -> int:
    return _any_int(10_000)


def _any_date() -> datetime.date:
    return datetime.date(
        year=random.randint(1990, 2030),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )


def _any_date_period() -> tuple[datetime.date, datetime.date | None]:
    start = _any_date()
    end = (
        datetime.date(
            year=random.randint(start.year + 1, 2030),
            month=random.randint(1, 12),
            day=random.randint(1, 28),
        )
        if random.choice([True, False])
        else None
    )
    return start, end


def _any_datetime() -> datetime.datetime:
    return tzdatetime(
        year=random.randint(1990, 2030),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )


def _any_bool() -> bool:
    return bool(random.getrandbits(1))


def _any_str(max_length: int = 32) -> str:
    return LOREM_IPSUM[random.randint(0, 100) : random.randint(120, 300)][:max_length]


def create_sample_person(
    parliamentdotuk: int | None = None,
    name: str | None = None,
    is_current: bool = True,
    is_active: bool = True,
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

    person = Person.objects.create(
        parliamentdotuk=m.pk,
        name=m.name,
        house=_coerce_house(m.house),
        **kwargs,
    )

    status, _ = PersonStatus.objects.get_or_create(
        person=person,
        defaults={"is_active": is_active, "is_current": is_current},
    )

    return person


def create_sample_constituency(
    name: str | None = None,
    parliamentdotuk: int | None = None,
    start: datetime.date | None = None,
    end: datetime.date | None = None,
    randomise: bool = True,
    mp: Person | None = None,
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
        mp=mp,
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
    name: str | None = None,
    parliamentdotuk: int | None = None,
    date: datetime.date | None = None,
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
        winner=mp,
    )


def create_constituency_result_detail(
    constituency: Constituency,
    election: Election,
    mp: Person,
    electorate: int | None = None,
    turnout: int | None = None,
    majority: int | None = None,
    result: str = "Party hold",
) -> ConstituencyResultDetail:
    """Create a ConstituencyResultDetail with custom data."""

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
        constituency_result=constituency_result,
        electorate=electorate,
        turnout=turnout,
        majority=majority,
        result=result,
    )


def create_sample_representative(
    person: Person | None = None,
    constituency: Constituency | None = None,
    start: datetime.date | None = None,
    end: datetime.date | None = None,
) -> ConstituencyRepresentative:
    if not start and not end:
        start, end = _any_date_period()

    return ConstituencyRepresentative.objects.create(
        person=person or create_sample_person(),
        constituency=constituency or create_sample_constituency(),
        start=start,
        end=end,
    )


def create_sample_party_demographics(
    party: Party,
    house: House = None,
    male_member_count: int = None,
    female_member_count: int = None,
    non_binary_member_count: int = None,
    total_member_count: int = None,
) -> PartyGenderDemographics:
    return PartyGenderDemographics.objects.create(
        party=party,
        house=house or create_sample_house(),
        male_member_count=(
            _any_int(200) if male_member_count is None else male_member_count
        ),
        female_member_count=(
            _any_int(200) if female_member_count is None else female_member_count
        ),
        non_binary_member_count=(
            _any_int(200)
            if non_binary_member_count is None
            else non_binary_member_count
        ),
        total_member_count=(
            _any_int(200) if total_member_count is None else total_member_count
        ),
    )


def create_sample_party(
    name: str | None = None,
    *,
    short_name: str | None = None,
    long_name: str | None = None,
    parliamentdotuk: int | None = None,
    homepage: str | None = None,
    wikipedia: str | None = None,
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

    party = Party.objects.create(
        name=party.name,
        parliamentdotuk=party.pk,
        short_name=short_name,
        long_name=long_name,
        homepage=homepage,
        wikipedia=wikipedia,
        year_founded=year_founded,
    )
    create_sample_party_demographics(party, _coerce_house("Commons"))
    create_sample_party_demographics(party, _coerce_house("Lords"))
    return party


def create_sample_parties():
    for x in SAMPLE_PARTIES:
        Party.objects.create(parliamentdotuk=x.pk, name=x.name)


def create_sample_session(
    name: str = "2017-2019",
    parliamentdotuk: int | None = None,
    start: datetime.date | None = None,
    end: datetime.date | None = None,
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
    parliamentdotuk: int | None = None,
    title: str = None,
    ayes: int = None,
    noes: int = None,
    did_not_vote: int = None,
    date: datetime.date = None,
    deferred_vote: bool = _any_bool(),
    session: ParliamentarySession | None = None,
    division_number: int = None,
) -> CommonsDivision:
    """Create a CommonsDivision with custom data."""
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not title:
        title = any_division_title()

    if not session:
        session = create_sample_session()

    if not ayes:
        ayes = _any_int(350)

    if not noes:
        noes = _any_int(350)

    if not did_not_vote:
        did_not_vote = _any_int(300)

    if not date:
        date = _any_date()

    if not division_number:
        division_number = _any_int(200)

    return CommonsDivision.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=title,
        ayes=ayes,
        noes=noes,
        is_passed=ayes > noes,
        did_not_vote=did_not_vote,
        date=date,
        is_deferred_vote=deferred_vote,
        session=session,
        division_number=division_number,
    )


def _coerce_house(house: str = "Commons") -> House:
    house, _ = House.objects.get_or_create(name=house)

    return house


def create_sample_house(name: str | None = None) -> House:
    if name is None:
        name = random.choice(["Commons", "Lords", "Unassigned"])

    house, _ = House.objects.get_or_create(name=name)

    return house


def create_sample_lords_division(
    parliamentdotuk: int | None = None,
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
        is_passed=ayes > noes,
        amendment_motion_notes=description,
        is_whipped=whipped_vote,
        number=division_number,
        is_government_content=_any_bool(),
        is_government_win=_any_bool(),
        division_had_tellers=_any_bool(),
        is_house=_any_bool(),
        teller_content_count=_any_bool(),
        teller_not_content_count=_any_bool(),
        member_content_count=_any_int(500),
        member_not_content_count=_any_int(500),
    )


def create_sample_bill_stage_type(
    parliamentdotuk: int | None = None,
    name: str | None = None,
    house: str | None = None,
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
    parliamentdotuk: int | None = None,
    name: str | None = None,
    description: str | None = None,
    category: BillTypeCategory | None = None,
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
    parliamentdotuk: int | None = None,
    title: str | None = None,
    long_title: str | None = None,
    last_update: datetime.datetime | None = None,
    bill_type: BillType | None = None,
) -> Bill:
    if not parliamentdotuk:
        parliamentdotuk = _any_id()

    if not title:
        title = _any_str()

    if not long_title:
        long_title = _any_str()

    if not last_update:
        last_update = _any_datetime()

    if not bill_type:
        bill_type = create_sample_bill_type()

    session = create_sample_session()

    bill = Bill.objects.create(
        parliamentdotuk=parliamentdotuk,
        title=title,
        long_title=long_title,
        summary=_any_str(),
        last_update=last_update,
        withdrawn_at=_any_datetime(),
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
    name: str | None = None,
    constituency_result_detail: ConstituencyResultDetail | None = None,
    party_name: str | None = None,
    order: int | None = None,
    votes: int | None = None,
    party: Party | None = any_sample_party(),
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

    if party_name:
        party = create_sample_party(name=party_name)

    return ConstituencyCandidate.objects.create(
        election_result=constituency_result_detail,
        name=name,
        votes=votes,
        order=order,
        party=party,
    )
