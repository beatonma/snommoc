from typing import Callable

from api import status
from crawlers.parliamentdotuk import tasks
from django.http import HttpRequest
from ninja import Router

router = Router(tags=["Tasks"])


def _start_task(func: Callable):
    """Start a celery task.

    Args:
        func: Must be annotated as a celery task.
    """
    func.delay()
    return status.HTTP_202_ACCEPTED, None


@router.post("update-active-members/")
def update_active_members(request: HttpRequest):
    return _start_task(tasks.update_profiles_for_active_members)


@router.post("update-divisions/")
def update_all_divisions(request: HttpRequest):
    return _start_task(tasks.update_all_divisions)


@router.post("update-election-results/")
def update_election_results(request: HttpRequest):
    return _start_task(tasks.update_election_results)


@router.post("update-member-portraits/")
def update_member_portraits(request: HttpRequest):
    return _start_task(tasks.update_member_portraits)


@router.post("update-bills/")
def update_bills(request: HttpRequest):
    return _start_task(tasks.update_bills)
