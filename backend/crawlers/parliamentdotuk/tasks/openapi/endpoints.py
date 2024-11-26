LORDS_DIVISIONS_ALL = "https://lordsvotes-api.parliament.uk/data/Divisions/search"
LORDS_DIVISION_SINGLE = (
    "https://lordsvotes-api.parliament.uk/data/Divisions/{division_id}"
)
COMMONS_DIVISIONS_ALL = (
    "https://commonsvotes-api.parliament.uk/data/divisions.json/search"
)
COMMONS_DIVISION_SINGLE = (
    "https://commonsvotes-api.parliament.uk/data/division/{division_id}.json"
)

BILLS_ALL = (
    "https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedDescending"
)
BILL_STAGE_DEFINITIONS = "https://bills-api.parliament.uk/api/v1/Stages"
BILL_TYPE_DEFINITIONS = "https://bills-api.parliament.uk/api/v1/BillTypes"
BILL_SINGLE = "https://bills-api.parliament.uk/api/v1/Bills/{bill_id}"
BILL_STAGES = "https://bills-api.parliament.uk/api/v1/Bills/{bill_id}/Stages"
BILL_PUBLICATIONS = (
    "https://bills-api.parliament.uk/api/v1/Bills/{bill_id}/Publications"
)

CONSTITUENCIES = "https://members-api.parliament.uk/api/Location/Constituency/Search"
CONSTITUENCY_BOUNDARY = "https://members-api.parliament.uk/api/Location/Constituency/{constituency_id}/Geometry"
CONSTITUENCY_RESULTS = "https://members-api.parliament.uk/api/Location/Constituency/{constituency_id}/ElectionResults"
CONSTITUENCY_RESULTS_FULL = "https://members-api.parliament.uk/api/Location/Constituency/{constituency_id}/ElectionResult/{election_id}"

MEMBER_PORTRAIT_URL = (
    "https://members-api.parliament.uk/api/Members/{member_id}/PortraitUrl"
)
MEMBERS_CURRENT = "https://members-api.parliament.uk/api/Members/Search"
MEMBERS_HISTORICAL = "https://members-api.parliament.uk/api/Members/SearchHistorical"
MEMBER_BIOGRAPHY = "https://members-api.parliament.uk/api/Members/{member_id}/Biography"
MEMBER_CONTACT = "https://members-api.parliament.uk/api/Members/{member_id}/Contact"
MEMBER_EXPERIENCE = (
    "https://members-api.parliament.uk/api/Members/{member_id}/Experience"
)
MEMBER_REGISTERED_INTERESTS = (
    "https://members-api.parliament.uk/api/Members/{member_id}/RegisteredInterests"
)
MEMBER_SUBJECTS_OF_INTEREST = (
    "https://members-api.parliament.uk/api/Members/{member_id}/Focus"
)


def constituency_boundary(constituency_id: int) -> str:
    return CONSTITUENCY_BOUNDARY.format(constituency_id=constituency_id)


def constituency_election_results(constituency_id: int) -> str:
    return CONSTITUENCY_RESULTS.format(constituency_id=constituency_id)


def constituency_election_results_detail(constituency_id: int, election_id: int) -> str:
    return CONSTITUENCY_RESULTS_FULL.format(
        constituency_id=constituency_id, election_id=election_id
    )


def lords_division(division_id: int) -> str:
    return LORDS_DIVISION_SINGLE.format(division_id=division_id)


def commons_division(division_id: int) -> str:
    return COMMONS_DIVISION_SINGLE.format(division_id=division_id)


def bill(bill_id: int) -> str:
    """Return API URL for a specific bill.

    Sample: https://bills-api.parliament.uk/api/v1/Bills/764
    """
    return BILL_SINGLE.format(bill_id=bill_id)


def bill_stages(bill_id: int) -> str:
    """Return API URL for stage data for a specific bill.

    Sample: https://bills-api.parliament.uk/api/v1/Bills/764/Stages
    """
    return BILL_STAGES.format(bill_id=bill_id)


def bill_publications(bill_id: int) -> str:
    """Return API URL for stage data for a specific bill.

    Sample: https://bills-api.parliament.uk/api/v1/Bills/512/Publications
    """
    return BILL_PUBLICATIONS.format(bill_id=bill_id)


def member_portrait(member_id: int) -> str:
    return MEMBER_PORTRAIT_URL.format(member_id=member_id)


def member_biography(member_id: int) -> str:
    return MEMBER_BIOGRAPHY.format(member_id=member_id)


def member_contact(member_id: int) -> str:
    return MEMBER_CONTACT.format(member_id=member_id)


def member_experience(member_id: int) -> str:
    return MEMBER_EXPERIENCE.format(member_id=member_id)


def member_registered_interests(member_id: int) -> str:
    return MEMBER_REGISTERED_INTERESTS.format(member_id=member_id)


def member_subjects_of_interest(member_id: int) -> str:
    return MEMBER_SUBJECTS_OF_INTEREST.format(member_id=member_id)
