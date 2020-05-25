"""

"""

import logging

from django.contrib import admin

from surface.models import (
    FeaturedPerson,
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
    MessageOfTheDay,
)

log = logging.getLogger(__name__)


@admin.register(FeaturedPerson, FeaturedBill, FeaturedCommonsDivision, FeaturedLordsDivision)
class FeaturedPersonAdmin(admin.ModelAdmin):
    pass


@admin.register(MessageOfTheDay)
class MessageOfTheDayAdmin(admin.ModelAdmin):
    pass
