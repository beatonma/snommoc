"""
Endpoints exposed by our server api
"""

import logging

log = logging.getLogger(__name__)

# Top level
CONSTITUENCY = 'constituency'
PARTY = 'party'
MEMBER = 'member'

# Member details
PROFILE = 'profile'
ADDRESS = 'address'
COMMITTEES = 'committees'
CONSTITUENCIES = 'constituencies'
CONTESTED_ELECTIONS = 'contested'
DECLARED_INTERESTS = 'interests'
ELECTIONS = 'elections'
EXPERIENCES = 'experiences'
MAIDEN_SPEECHES = 'speeches'
PARTIES = 'parties'
POSTS = 'posts'
SUBJECTS_OF_INTEREST = 'subjects'


def endpoint_list(endpoint_name):
    return f'{endpoint_name}-list'


def endpoint_detail(endpoint_name):
    return f'{endpoint_name}-detail'
