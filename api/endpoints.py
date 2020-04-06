"""
Endpoints exposed by our server api
"""

import logging

log = logging.getLogger(__name__)

_HOUSE_COMMONS = 'commons'
_HOUSE_LORDS = 'lords'

# Top level
CONSTITUENCY = 'constituency'
PARTY = 'party'
MEMBER = 'member'
DIVISIONS = 'division'

# Member details
MEMBER_FULL_PROFILE = f'{MEMBER}/profile'
MEMBER_VOTES = f'{MEMBER}/votes'

# Divisions
DIVISION_COMMONS = f'{DIVISIONS}/{_HOUSE_COMMONS}'
DIVISION_LORDS = f'{DIVISIONS}/{_HOUSE_LORDS}'

# Bills
BILL = 'bill'

# Featured
FEATURED = 'featured'
FEATURED_MEMBERS = f'{FEATURED}/members'
FEATURED_BILLS = f'{FEATURED}/bills'
FEATURED_DIVISIONS = f'{FEATURED}/divisions'


def endpoint_list(endpoint_name):
    return f'{endpoint_name}-list'


def endpoint_detail(endpoint_name):
    return f'{endpoint_name}-detail'
