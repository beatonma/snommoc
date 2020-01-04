"""
Sample response:
    "CurrentStatus": {
        "@Id": "0",
        "@IsActive": "True",
        "Name": "Current Member",
        "Reason": null,
        "StartDate": "2019-12-12T00:00:00"
    }
"""

import logging

log = logging.getLogger(__name__)


CURRENT_STATUS = 'CurrentStatus'
IS_ACTIVE = '@IsActive'
START_DATE = 'StartDate'
