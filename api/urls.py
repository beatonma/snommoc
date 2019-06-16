from django.urls import path

from api.views.people import GetMpView

urlpatterns = [
    path('get_mp', GetMpView.as_view(), name='get_mp_view'),
]
