"""
Data crawlers for OpenAPI sources listed at https://developer.parliament.uk/

These should replace LDA APIs for bills and divisions, and may also replace the members data platform (MDP) for member data..
"""

from .bills import update_bills
from .divisions import update_lords_divisions
