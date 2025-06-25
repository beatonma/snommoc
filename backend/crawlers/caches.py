"""
Cache names used for JsonCache (usually via @task_context decorator)
"""

BILLS = "bills"
CONSTITUENCIES = "constituencies"
COMMONS_DIVISIONS = "divisions-commons"
LORDS_DIVISIONS = "divisions-lords"
ELECTION_RESULTS = "election-results"
MEMBERS = "members"
MEMBER_PORTRAITS = "memberportraits"
DEMOGRAPHICS = "demographics"
WIKIPEDIA = "wikipedia"


# Key used to invalidate cached API responses when a crawler task completes.
API_VIEW_CACHE = "crawlers_view_cache"
