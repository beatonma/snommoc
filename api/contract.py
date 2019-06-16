"""Standard key names for JSON responses returned by this API,
or GET parameters in requests.
"""

""""
Example MP API response::
    {
        NAME: str,
        ALIASES: List[str],
        THEYWORKFORYOU_ID: int,
        PARLIAMENTDOTUK_ID: int,
        PARTY: str,
        CONSTITUENCY: str,

        INTERESTS: Dict {
            INTERESTS_POLITICAL: List[str],
            INTERESTS_COUNTRIES: List[str]
        },

        PERSONAL_LINKS: Dict {
            EMAIL: str,
            WIKIPEDIA: str,
            PHONE: Dict {
                PHONE_CONSTITUENCY: str,
                PHONE_PARLIAMENT: str
            },
            WEBLINKS: List[str]
        }
    }
"""

# Identifying info
NAME = 'name'
ALIASES = 'aliases'
THEYWORKFORYOU_ID = 'theyworkforyou'
PARLIAMENTDOTUK_ID = 'parliamentdotuk'

# Political affiliations
PARTY = 'party'
PARTY_LONG = 'party_longname'
PARTY_SHORT = 'party_shortname'
CONSTITUENCY = 'constituency'

# Interests
INTERESTS = 'interests'
INTERESTS_POLITICAL = 'interests_political'
INTERESTS_COUNTRIES = 'interests_countries'

# Contact/links
PERSONAL_LINKS = 'links'
EMAIL = 'email'
WEBLINKS = 'weblinks'
WIKIPEDIA = 'wikipedia'
PHONE = 'phone'
PHONE_CONSTITUENCY = 'phone_constituency'
PHONE_PARLIAMENT = 'phone_parliamentary'


# API
API_KEY = 'key'
