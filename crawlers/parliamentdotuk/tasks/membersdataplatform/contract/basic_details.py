"""
Sample response:
    BasicDetails": {
        "GivenSurname": "Wrigglesworth",
        "GivenMiddleNames": null,
        "GivenForename": "Ian",
        "TownOfBirth": null,
        "CountryOfBirth": null,
        ...
    }
"""

import logging

log = logging.getLogger(__name__)

BASIC_DETAILS = 'BasicDetails'

SURNAME = 'GivenSurname'
MIDDLE_NAMES = 'GivenMiddleNames'
FORENAME = 'GivenForename'
TOWN_OF_BIRTH = 'TownOfBirth'
COUNTRY_OF_BIRTH = 'CountryOfBirth'
