LORDS_DIVISIONS_ALL = "https://lordsvotes-api.parliament.uk/data/Divisions/search"
LORDS_DIVISION_SINGLE = "https://lordsvotes-api.parliament.uk/data/Divisions/{id}"

BILLS_ALL = (
    "https://bills-api.parliament.uk/api/v1/Bills?SortOrder=DateUpdatedDescending"
)
BILL_SINGLE = "https://bills-api.parliament.uk/api/v1/Bills/{id}"


def lords_division(id: int) -> str:
    return LORDS_DIVISION_SINGLE.format(id=id)


def bill(id: int) -> str:
    return BILL_SINGLE.format(id=id)
