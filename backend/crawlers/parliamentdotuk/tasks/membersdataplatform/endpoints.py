_BASE_URL = (
    "https://data.parliament.uk/membersdataplatform/services/mnis/members/query/"
)


def _get_endpoint(query: str, outputs: str = None) -> str:
    url = f"{_BASE_URL}{query}/"
    if outputs:
        url += f"{outputs}/"
    return url


COMMONS_MEMBERS_ALL = _get_endpoint(query="House=Commons|membership=all")
LORDS_MEMBERS_ALL = _get_endpoint(query="House=Lords|membership=all")

MEMBER_PORTRAIT_URL = "https://members-api.parliament.uk/api/Members/{id}/PortraitUrl"


def member_biography(parliamentdotuk: int):
    return _get_endpoint(f"id={parliamentdotuk}", outputs="FullBiog")
