from django.urls import path

from crawlers.parliamentdotuk.views.update_constituencies import (
    UpdateConstituenciesView,
    VIEW_UPDATE_CONSTITUENCIES,
)

urlpatterns = [
    path('constituencies/', UpdateConstituenciesView.as_view(), name=VIEW_UPDATE_CONSTITUENCIES),
]
