"""

"""

import logging

from django.contrib import admin
from django.utils.safestring import mark_safe

from crawlers.parliamentdotuk.models import (
    BillUpdateError,
    CommonsDivisionUpdateError,
    ElectionResultUpdateError,
    LordsDivisionUpdateError,
)
from crawlers.parliamentdotuk.tasks.lda import endpoints


log = logging.getLogger(__name__)


@admin.register(
    BillUpdateError,
    CommonsDivisionUpdateError,
    ElectionResultUpdateError,
    LordsDivisionUpdateError,
)
class UpdateErrorAdmin(admin.ModelAdmin):
    def source_url(self, obj):
        """Add a link to the API page that was being read when the error occurred."""
        if isinstance(obj, BillUpdateError):
            url = endpoints.url_for_bill(obj.parliamentdotuk)
        elif isinstance(obj, CommonsDivisionUpdateError):
            url = endpoints.url_for_commons_division(obj.parliamentdotuk)
        elif isinstance(obj, LordsDivisionUpdateError):
            url = endpoints.url_for_lords_division(obj.parliamentdotuk)
        elif isinstance(obj, ElectionResultUpdateError):
            url = endpoints.url_for_election_result(obj.parliamentdotuk)
        else:
            url = "UNHANDLED TYPE"

        return mark_safe(f'<a href="{url}">{url}</a>')

    fields = [
        "handled",
        "created_on",
        "parliamentdotuk",
        "error_message",
        "trace",
        "source_url",
    ]

    list_display = [
        "error_message",
        "handled",
    ]

    readonly_fields = [
        "created_on",
        "parliamentdotuk",
        "error_message",
        "trace",
        "source_url",
    ]
