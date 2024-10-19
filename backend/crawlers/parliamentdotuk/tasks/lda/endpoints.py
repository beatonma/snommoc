CONSTITUENCIES_BASE_URL = "https://lda.data.parliament.uk/constituencies.json"

# E.g. https://lda.data.parliament.uk/commonsdivisions/id/1171292.json
COMMONS_DIVISIONS = "https://lda.data.parliament.uk/commonsdivisions.json"
COMMONS_DIVISION = (
    "https://lda.data.parliament.uk/commonsdivisions/id/{parliamentdotuk}.json"
)

# e.g. https://lda.data.parliament.uk/electionresults/382387.json
ELECTION_RESULTS = "https://lda.data.parliament.uk/electionresults.json"
ELECTION_RESULT_DETAIL = (
    "https://lda.data.parliament.uk/electionresults/{parliamentdotuk}.json"
)

# RSS
CALENDAR = "https://services.parliament.uk/calendar/all.rss"


PARAM_PAGE_SIZE = "_pageSize"
PARAM_PAGE = "_page"
MAX_PAGE_SIZE = 500


def url_for_commons_division(parliamentdotuk: int) -> str:
    return COMMONS_DIVISION.format(parliamentdotuk=parliamentdotuk)


def url_for_election_result(parliamentdotuk: int) -> str:
    return ELECTION_RESULT_DETAIL.format(parliamentdotuk=parliamentdotuk)


def debug_url(base: str, **params) -> str:
    param_str = "&".join([f"{key}={value}" for (key, value) in params.items()])
    return f"{base}?{param_str}"
