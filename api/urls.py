from django.urls import path

from api.views.parties import (
    VIEW_GET_PARTIES,
    GetPartiesView,
)
from api.views.people import (
    GetMpView,
    GetAllMPsView,
    VIEW_GET_ALL_MPS,
    VIEW_GET_MP,
)

urlpatterns = [
    path('get_mp', GetMpView.as_view(), name=VIEW_GET_MP),
    path('get_all_mps', GetAllMPsView.as_view(), name=VIEW_GET_ALL_MPS),
    path('get_parties', GetPartiesView.as_view(), name=VIEW_GET_PARTIES),
]
