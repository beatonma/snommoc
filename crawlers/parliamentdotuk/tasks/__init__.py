from repository.models import (
    Constituency,
    # Mp,
    Person,
    Party,
)
from repository.tasks import init_parties
from .lda.update_constituencies import update_constituencies
# from .lda.update_mps import update_mps
from .membersdataplatform import update_all_member_data


def update_parliament_data():
    update_constituencies()
    # update_mps()


def clear_parliament_data():
    # Mp.objects.all().delete()
    Party.objects.all().delete()
    Person.objects.all().delete()
    Constituency.objects.all().delete()


def rebuild_all_data():
    clear_parliament_data()
    init_parties()
    update_constituencies()
    update_all_member_data()
