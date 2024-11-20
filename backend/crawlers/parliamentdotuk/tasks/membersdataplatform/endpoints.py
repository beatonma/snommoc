COMMONS_MEMBERS_ALL = "https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons|membership=all/"
LORDS_MEMBERS_ALL = "https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords|membership=all/"


def member_biography(parliamentdotuk: int):
    return f"https://data.parliament.uk/membersdataplatform/services/mnis/members/query/id={parliamentdotuk}/FullBiog/"


MEMBER_PORTRAIT_URL = "https://members-api.parliament.uk/api/Members/{id}/PortraitUrl"
