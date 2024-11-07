from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render
from django.views import View


class StaffView(UserPassesTestMixin, View):
    """Dashboard is only viewable by staff accounts."""

    def test_func(self):
        return self.request.user.is_staff


class DashboardView(StaffView):
    def get(self, request):
        return render(
            request,
            "dashboard.html",
        )
