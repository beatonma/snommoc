"""
Data crawlers for OpenAPI sources listed at https://developer.parliament.uk/

These should replace LDA APIs for bills and divisions.
"""

from .bills import update_bills
from .constituencies import (
    update_constituencies,
    update_constituency_boundaries,
    update_election_results,
)
from .divisions import update_lords_divisions
from .members import update_current_members
