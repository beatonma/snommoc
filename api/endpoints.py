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
PROFILE = f'{MEMBER}/profile'
ADDRESS = f'{MEMBER}/address'
COMMITTEES = f'{MEMBER}/committees'
CONSTITUENCIES = f'{MEMBER}/constituencies'
CONTESTED_ELECTIONS = f'{MEMBER}/contested'
DECLARED_INTERESTS = f'{MEMBER}/interests'
ELECTIONS = f'{MEMBER}/elections'
EXPERIENCES = f'{MEMBER}/experiences'
MAIDEN_SPEECHES = f'{MEMBER}/speeches'
PARTIES = f'{MEMBER}/parties'
POSTS = f'{MEMBER}/posts'
SUBJECTS_OF_INTEREST = f'{MEMBER}/subjects'
VOTES = f'{MEMBER}/votes'

# Divisions
DIVISION_COMMONS = f'{DIVISIONS}/{_HOUSE_COMMONS}'
DIVISION_LORDS = f'{DIVISIONS}/{_HOUSE_LORDS}'

# Bills
BILL = 'bill'

# Featured
FEATURED = 'featured'


def endpoint_list(endpoint_name):
    return f'{endpoint_name}-list'


def endpoint_detail(endpoint_name):
    return f'{endpoint_name}-detail'
