"""

"""

import logging

from repository.models import Party

log = logging.getLogger(__name__)


PARTY_DEFINITIONS = [
    # (common_name, official_name, abbreviation)

    # Parties that currently (11/2019) have seats in the Commons
    ('Conservative', 'Conservative and Unionist Party', 'Con', 1834, 'https://www.conservatives.com/'),
    ('Labour', 'Labour Party', 'Lab', 1900, 'https://labour.org.uk/'),
    ('SNP', 'Scottish National Party', 'SNP', 1934, 'https://www.snp.org/'),
    ('Independent', 'Independent', 'Indie', 0, None),
    ('Lib Dem', 'Liberal Democrats', 'LD', 1988, 'https://www.libdems.org.uk/'),
    ('DUP', 'Democratic Unionist Party', 'DUP', 1971, 'https://www.mydup.com/'),
    ('Sinn Féin', 'Sinn Féin', 'SF', 1905, 'https://www.sinnfein.ie/'),
    ('Change UK', 'The Independent Group for Change', 'TIG', 2019, 'https://voteforchange.uk/'),
    ('Plaid Cymru', 'Plaid Cymru – The Party of Wales', 'Plaid', 1925, 'https://www.plaid.cymru/'),
    ('Green Party', 'Green Party of England and Wales', 'Green', 1990, 'https://www.greenparty.org.uk/'),

    # Parties that had seats in the previous Parliament but not now
    ('SDLP', 'Social Democratic and Labour Party', 'SDLP', 1970, 'https://www.sdlp.ie/'),
    ('UUP', 'Ulster Unionist Party', 'UUP', 1905, 'https://www.uup.org/'),
    ('UKIP', 'UK Independence Party', 'UKIP', 1993, 'https://www.ukip.org/'),

    # Other entities
    ('Speaker', 'Speaker', 'Speaker', 1377, 'https://www.parliament.uk/business/commons/the-speaker/'),
]


def init_parties():
    for (
            name,
            long_name,
            abbreviation,
            year_founded,
            homepage
    ) in PARTY_DEFINITIONS:
        Party.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'long_name': long_name,
                'short_name': abbreviation,
                'year_founded': year_founded,
                'homepage': homepage
            }
        )
