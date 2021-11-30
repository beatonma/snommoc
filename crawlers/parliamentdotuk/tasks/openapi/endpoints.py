LORDS_DIVISIONS_ALL = "https://lordsvotes-api.parliament.uk/data/Divisions/search"
LORDS_DIVISION_SINGLE = "https://lordsvotes-api.parliament.uk/data/Divisions/{id}"


def lords_division(id: int) -> str:
    return LORDS_DIVISION_SINGLE.format(id=id)
