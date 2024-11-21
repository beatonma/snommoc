# E.g. https://lda.data.parliament.uk/commonsdivisions/id/1171292.json
COMMONS_DIVISIONS = "https://lda.data.parliament.uk/commonsdivisions.json"
COMMONS_DIVISION = (
    "https://lda.data.parliament.uk/commonsdivisions/id/{parliamentdotuk}.json"
)


# RSS
CALENDAR = "https://services.parliament.uk/calendar/all.rss"


def url_for_commons_division(parliamentdotuk: int) -> str:
    return COMMONS_DIVISION.format(parliamentdotuk=parliamentdotuk)
