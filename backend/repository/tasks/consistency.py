"""
Basic consistency checks to make sure our data makes sense.
"""

import colorama
from django.apps import apps
from django.db.models import F

from repository.models import Constituency, Person
from repository.resolution import (
    get_active_constituencies,
    get_active_mps,
)


def check_consistency():
    _check_constituencies()
    _check_members()
    _check_model_instances()
    _recent_changes()


def _check_constituencies():
    """
    Check how many constituencies are currently active, compared to the expected count of 650.
    Check for any active constituencies that do not have an MP associated with them.
    Check for any constituencies that have null start dates.
    """
    active_constituencies = get_active_constituencies()
    missing_mps = active_constituencies.filter(mp__isnull=True)

    print(f"Active constituencies: {active_constituencies.count()}/650 (expected)")
    print("")

    if missing_mps:
        _print_list(
            f"There are {missing_mps.count()} active constituencies with no MP:",
            missing_mps,
        )

    missing_data_constituencies = Constituency.objects.filter(start__isnull=True)
    if missing_data_constituencies:
        _print_list(
            f"There are {missing_data_constituencies.count()} constituencies with missing data:",
            missing_data_constituencies,
        )


def _check_members():
    """
    Check how many members are marked as active, compared to the expected count of 650.
    Check for any active MPs that do not have an associated constituency.
    """
    active_mps = get_active_mps()

    print(f"Active MPs: {active_mps.count()}/650 (expected)")
    print("")

    active_mps_with_no_constituency = active_mps.filter(constituency__isnull=True)
    if active_mps_with_no_constituency:
        _print_list(
            f"There are {active_mps_with_no_constituency.count()} active MPs who do not have an associated constituency!",
            active_mps_with_no_constituency,
        )


def _check_model_instances():
    models = apps.get_app_config("repository").get_models()

    empty = [m for m in models if m.objects.count() == 0]

    _print_list("Models with zero instances", empty)


def _recent_changes():
    latest_people = _get_latest_creations(Person)
    latest_modified_people = _get_latest_modified(Person)

    _print_list(
        "Newest people", latest_people, lambda x: f"{x} ({_date(x.created_on)})"
    )

    _print_list(
        "Recently modified",
        latest_modified_people,
        lambda x: f"{x} ({_date(x.modified_on)})",
    )


def _get_latest_creations(Model):
    """
    Return the 5 most recently created instances of the given model.
    Model must be a subclass of BaseModel, or otherwise have a created_on DateTimeField.
    """
    return Model.objects.order_by("-created_on")[:5]


def _get_latest_modified(Model):
    """
    Return the 5 most recently modified instances of the given model.
    Model must be a subclass of BaseModel, or otherwise have DateTimeField fields named created_on, modified_on.
    :param Model:
    :return:
    """
    return Model.objects.exclude(modified_on=F("created_on")).order_by("-modified_on")[
        :5
    ]


def _print_list(title, lst, list_func=None):
    def println(text):
        print(f"- {text}")

    def print_title(text):
        print(f"{colorama.Fore.LIGHTBLUE_EX}{text}{colorama.Fore.RESET}")

    print_title(title)

    if lst:
        for x in lst:
            if list_func:
                println(list_func(x))
            else:
                println(x)
    else:
        println("(None)")

    print("")


def _date(dt):
    return dt.strftime("%Y-%m-%d")
