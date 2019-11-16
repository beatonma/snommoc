from repository.models import (
    Constituency,
    Mp,
)
from .lda.update_constituencies import update_constituencies
from .lda.update_mps import update_mps


def update_parliament_data():
    update_constituencies()
    update_mps()


def clear_parliament_data():
    Mp.objects.all().delete()
    Constituency.objects.all().delete()
