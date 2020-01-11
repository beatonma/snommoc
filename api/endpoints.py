"""
Endpoints exposed by our server api
"""

import logging

log = logging.getLogger(__name__)

CONSTITUENCY = 'constituency'
PARTY = 'party'
MEMBER = 'member'


def endpoint_list(endpoint_name):
    return f'{endpoint_name}-list'


def endpoint_detail(endpoint_name):
    return f'{endpoint_name}-detail'
