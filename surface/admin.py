from django.contrib import admin

from surface.models import (
    FeaturedBill,
    FeaturedCommonsDivision,
    FeaturedLordsDivision,
    FeaturedPerson,
    MessageOfTheDay,
)


@admin.register(
    FeaturedPerson, FeaturedBill, FeaturedCommonsDivision, FeaturedLordsDivision
)
class FeaturedPersonAdmin(admin.ModelAdmin):
    pass


@admin.register(MessageOfTheDay)
class MessageOfTheDayAdmin(admin.ModelAdmin):
    pass
