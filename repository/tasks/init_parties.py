"""

"""

import logging

from repository.models import Party

log = logging.getLogger(__name__)


PARTY_DEFINITIONS = [
    # UPDATED January 2020
    # (common_name, official_name, abbreviation, year_founded, homepage, wikipedia)

    # Parties that currently have seats in the Commons
    ('Conservative', 'Conservative and Unionist Party', 'Con', 1834, 'https://www.conservatives.com/', 'Conservative_Party_(UK)'),
    ('Labour', 'Labour Party', 'Lab', 1900, 'https://labour.org.uk/', 'Labour_Party_(UK)'),
    ('SNP', 'Scottish National Party', 'SNP', 1934, 'https://www.snp.org/', 'Scottish_National_Party'),
    ('Independent', 'Independent', 'Indie', 0, None, 'Independent_politician'),
    ('Lib Dem', 'Liberal Democrats', 'LD', 1988, 'https://www.libdems.org.uk/', 'Liberal_Democrats_(UK)'),
    ('DUP', 'Democratic Unionist Party', 'DUP', 1971, 'https://www.mydup.com/', 'Democratic_Unionist_Party'),
    ('Sinn Féin', 'Sinn Féin', 'SF', 1905, 'https://www.sinnfein.ie/', 'Sinn_Féin'),
    ('Plaid Cymru', 'Plaid Cymru – The Party of Wales', 'Plaid', 1925, 'https://www.plaid.cymru/', 'Plaid_Cymru'),
    ('Green Party', 'Green Party of England and Wales', 'Green', 1990, 'https://www.greenparty.org.uk/', 'Green_Party_of_England_and_Wales'),
    ('SDLP', 'Social Democratic and Labour Party', 'SDLP', 1970, 'https://www.sdlp.ie/', 'Social_Democratic_and_Labour_Party'),
    ('Alliance', 'Alliance Party of Northern Ireland', 'APNI', 1970, 'https://www.allianceparty.org/', 'Alliance_Party_of_Northern_Ireland'),

    # Other parties of prominence that have held seats in recent years but not now
    ('Change UK', 'The Independent Group for Change', 'TIG', 2019, 'https://voteforchange.uk/', 'Change_UK'),
    ('UUP', 'Ulster Unionist Party', 'UUP', 1905, 'https://www.uup.org/', 'Ulster_Unionist_Party'),
    ('UKIP', 'UK Independence Party', 'UKIP', 1993, 'https://www.ukip.org/', 'UK_Independence_Party'),

    # Other entities
    ('Speaker', 'Speaker', 'Speaker', 1377, 'https://www.parliament.uk/business/commons/the-speaker/', 'Speaker_of_the_House_of_Commons_(United_Kingdom)'),
]


def init_parties():
    for (
            name,
            long_name,
            abbreviation,
            year_founded,
            homepage,
            wikipedia
    ) in PARTY_DEFINITIONS:
        Party.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'long_name': long_name,
                'short_name': abbreviation,
                'year_founded': year_founded,
                'homepage': homepage,
                'wikipedia': wikipedia,
            }
        )
