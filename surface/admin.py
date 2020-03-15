"""

"""

import logging

from django.contrib import admin

from surface.models import (
    FeaturedPerson,
    FeaturedBill,
)

log = logging.getLogger(__name__)


@admin.register(FeaturedPerson, FeaturedBill)
class FeaturedPersonAdmin(admin.ModelAdmin):
    pass
