"""
Post-processing tasks
"""

import logging

from django.db.models import Q

from repository.models import (
    Constituency,
    ConstituencyResult,
)
from repository.models.constituency import ConstituencyAlsoKnownAs

log = logging.getLogger(__name__)


def _first_true(iterable, default=None, pred=lambda x: x is not None):
    """Returns the first true value in the iterable.

    See https://docs.python.org/3/library/itertools.html#itertools-recipes

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def _consolidate(real, pretender) -> bool:
    real.mp = _first_true([real.mp, pretender.mp])
    pretender.mp = None  # MP can only be associated with one Constituency

    real.gss_code = _first_true([real.gss_code, pretender.gss_code])
    real.ordinance_survey_name = _first_true([real.ordinance_survey_name, pretender.ordinance_survey_name])
    real.start = _first_true([real.start, pretender.start])
    real.end = _first_true([real.end, pretender.end])
    real.constituency_type = _first_true([real.constituency_type, pretender.constituency_type])

    pretender.save()
    real.save()
    c, created = ConstituencyAlsoKnownAs.objects.update_or_create(
        alias=pretender,
        defaults={
            'canonical': real,
        }
    )
    return created


def consolidate_constituencies():
    """Constituency data returned from the LDA API do not have IDs to match
    those from the MDP API. Here we try to recognise matching results from
    the two sources and consolidate their content into a canonical object under
    the MDP API ID schema.

    LDA constituencies have (or potentially have) name, mp, start/end dates,
    gss code, os name, constituency_type

    MDP constituencies only have a name.
    """
    relations_created = 0
    constituency_results = ConstituencyResult.objects.all()

    for result in constituency_results:
        canonical = result.constituency
        constituency_name = canonical.name

        election_date = result.election.date

        candidates = Constituency.objects.filter(
            start__lte=election_date
        ).filter(
            Q(end__isnull=True) | Q(end__gt=election_date)
        ).filter(name__icontains=constituency_name).exclude(
            parliamentdotuk=canonical.parliamentdotuk
        )

        population = candidates.count()

        if population > 1:
            candidates = candidates.filter(name=constituency_name)
            population = candidates.count()

        if population == 1:
            created = _consolidate(canonical, candidates.first())
            if created:
                relations_created = relations_created + 1

        elif population == 0:
            print(f'{election_date} No candidates found for {constituency_name} '
                  f'{canonical.parliamentdotuk}')

        else:
            print(f'{election_date} {population} candidates found for '
                  f'{constituency_name} - further pruning required:')
            for x in candidates:
                print(f'  {x}')
            input('continue')

    log.info(f'Complete: created {relations_created} new relations.')
