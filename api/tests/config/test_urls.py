from django.urls import path

from api.tests.views import ExampleView

from api.urls import urlpatterns

urlpatterns += [
    path('decorator', ExampleView.as_view(), name='decorator_test_view'),
]
