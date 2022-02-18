LORDS_DIVISIONS_ALL = "https://lordsvotes-api.parliament.uk/data/Divisions/search"
LORDS_DIVISION_SINGLE = (
    "https://lordsvotes-api.parliament.uk/data/Divisions/{division_id}"
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


def lords_division(division_id: int) -> str:
    return LORDS_DIVISION_SINGLE.format(division_id=division_id)


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
