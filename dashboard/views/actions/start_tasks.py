from django.http import HttpResponse

from crawlers.parliamentdotuk.tasks import (
    update_all_divisions,
    update_election_results,
    update_member_portraits,
    update_profiles_for_active_members,
)
from crawlers.parliamentdotuk.tasks.openapi.bills import update_bills
from dashboard.views.dashboard import StaffView


class _TaskView(StaffView):
    func = None

    def post(self, request, *args, **kwargs):
        self.func.delay()
        return HttpResponse(status=204)


class UpdateProfilesTaskView(_TaskView):
    func = update_profiles_for_active_members


class UpdatePortraitsTaskView(_TaskView):
    func = update_member_portraits


class UpdateBillsTaskView(_TaskView):
    func = update_bills


class UpdateDivisionsTaskView(_TaskView):
    func = update_all_divisions


class UpdateElectionResultsTaskView(_TaskView):
    func = update_election_results
