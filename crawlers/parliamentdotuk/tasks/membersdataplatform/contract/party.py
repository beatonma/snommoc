"""
Sample response:
    "Party": {
        "@Id": "15",
        "#text": "Labour"
    }
"""

import logging

log = logging.getLogger(__name__)

PARTIES = 'Parties'
PARTY = 'Party'
GROUP_KEY = f'{PARTIES}.{PARTY}'

PARTY_NAME = 'Name'
START_DATE = 'StartDate'
END_DATE = 'EndDate'
