"""

"""

import logging

from django.shortcuts import render

from dashboard.views.dashboard import StaffView
from repository.models import Person

log = logging.getLogger(__name__)


class MemberProfileView(StaffView):
    def get(self, request, *args, **kwargs):
        member = Person.objects.get(parliamentdotuk=kwargs.get('pk'))
        print(member)
        return render(
            request,
            'dashboard-member-profile.html',
            {
                'member': member,
            }
        )
