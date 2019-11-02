"""

"""

import logging

from repository.models import Party

log = logging.getLogger(__name__)


PARTY_DEFINITIONS = [
    # (common_name, official_name, abbreviation)

    # Parties that currently (11/2019) have seats in the Commons
    ('Conservative', 'Conservative and Unionist Party', 'Con'),
    ('Labour', 'Labour Party', 'Lab'),
    ('SNP', 'Scottish National Party', 'SNP'),
    ('Independent', 'Independent', 'Indie'),
    ('Lib Dem', 'Liberal Democrats', 'LD'),
    ('DUP', 'Democratic Unionist Party', 'DUP'),
    ('Sinn Féin', 'Sinn Féin', 'SF'),
    ('Change UK', 'The Independent Group for Change', 'TIG'),
    ('Plaid Cymru', 'Plaid Cymru – The Party of Wales', 'Plaid'),
    ('Green Party', 'Green Party of England and Wales', 'Green'),

    # Parties that had seats in the previous Parliament but not now
    ('SDLP', 'Social Democratic and Labour Party', 'SDLP'),
    ('UUP', 'Ulster Unionist Party', 'UUP'),
    ('UKIP', 'UK Independence Party', 'UKIP'),

    # Other entities
    ('Speaker', 'Speaker', 'Speaker'),
]


def init_parties():
    for (name, long_name, abbreviation) in PARTY_DEFINITIONS:
        Party.objects.create(
            name=name,
            long_name=long_name,
            short_name=abbreviation
        ).save()
