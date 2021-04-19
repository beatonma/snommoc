"""

"""

import logging

from django.shortcuts import redirect
from django.utils.datetime_safe import datetime

from dashboard.views.dashboard import StaffView
from surface.models import (
    FeaturedPerson,
    FeaturedBill,
)

log = logging.getLogger(__name__)


class AddFeaturedMemberView(StaffView):
    def get(self, request, *args, **kwargs):
        parliamentdotuk = request.GET.get('id')
        FeaturedPerson.objects.create(
            person_id=parliamentdotuk,
            start=datetime.today()
        ).save()

        return redirect('dashboard')


class AddFeaturedBillView(StaffView):
    def get(self, request, *args, **kwargs):
        parliamentdotuk = request.GET.get('id')
        FeaturedBill.objects.create(
            bill_id=parliamentdotuk,
            start=datetime.today()
        ).save()

        return redirect('dashboard')
