from repository.models import (
    Constituency,
    Person,
    Party,
)
from repository.tasks import init_parties
from .lda.update_constituencies import update_constituencies
from .membersdataplatform import update_all_member_data


def clear_parliament_data():
    Party.objects.all().delete()
    Person.objects.all().delete()
    Constituency.objects.all().delete()


def rebuild_all_data():
    clear_parliament_data()
    init_parties()
    update_constituencies()
    update_all_member_data()
