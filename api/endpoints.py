"""
Endpoints exposed by our server api
"""
from api import contract

PING = "ping/"

# Top level
CONSTITUENCY = "constituency"
PARTY = "party"
MEMBER = "member"
DIVISIONS = "division"

# Constituency
MEMBER_FOR_CONSTITUENCY = f"{CONSTITUENCY}/member"
CONSTITUENCY_RESULTS = f"{CONSTITUENCY}/<int:pk>/election/<int:election_id>/"

# Member details
MEMBER_FULL_PROFILE = MEMBER
MEMBER_VOTES = f"{MEMBER}/votes"

# Divisions
DIVISION_COMMONS = f"{DIVISIONS}/{contract.HOUSE_COMMONS}"
DIVISION_LORDS = f"{DIVISIONS}/{contract.HOUSE_LORDS}"

# Bills
BILL = "bill"

# Timely stuff e.g. trending people
ZEITGEIST = "zeitgeist"

# Server internals/admin stuff
MOTD = f"motd"


def endpoint_list(endpoint_name):
    return f"{endpoint_name}-list"


def endpoint_detail(endpoint_name):
    return f"{endpoint_name}-detail"


def endpoint_name(endpoint_name):
    """Sanitize name for use as view name for reverse lookup via urlpatterns."""
    return endpoint_name.replace(":", "-")
