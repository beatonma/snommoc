"""

"""

import logging

from django.contrib import admin

from crawlers.parliamentdotuk.models import (
    BillUpdateError,
    CommonsDivisionUpdateError,
    LordsDivisionUpdateError,
)

log = logging.getLogger(__name__)


@admin.register(
    BillUpdateError,
    CommonsDivisionUpdateError,
    LordsDivisionUpdateError,
)
class UpdateErrorAdmin(admin.ModelAdmin):
    list_display = [
        'error_message',
        'handled',
    ]
