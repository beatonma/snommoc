COMMONS_MEMBERS_ALL = "https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons|membership=all/"
LORDS_MEMBERS_ALL = "https://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords|membership=all/"


def member_biography(parliamentdotuk: int):
    return f"https://data.parliament.uk/membersdataplatform/services/mnis/members/query/id={parliamentdotuk}/FullBiog/"
