"""

"""

import logging

from django.contrib import admin

from surface.models import (
    FeaturedPerson,
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
)

log = logging.getLogger(__name__)


@admin.register(FeaturedPerson, FeaturedBill, FeaturedCommonsDivision, FeaturedLordsDivision)
class FeaturedPersonAdmin(admin.ModelAdmin):
    pass
