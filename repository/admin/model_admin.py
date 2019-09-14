from django.contrib import admin
from django.contrib.contenttypes.admin import (
    GenericStackedInline,
    GenericTabularInline,
)

from repository.models import (
    Constituency,
    Interest,
)
from repository.models.contact_details import (
    PersonalLinks,
    WebLink,
)
from repository.models import (
    Mp,
    Party,
)
# from repository.models.interests import (
#     CountryOfInterest,
#     PoliticalInterest,
# )


class PersonalLinksInline(GenericStackedInline):
    model = PersonalLinks
    ct_field = 'person_content_type'
    ct_fk_field = 'person_id'
    max_num = 1


class InterestInline(GenericTabularInline):
    model = Interest
    ct_field = 'person_content_type'
    ct_fk_field = 'person_id'


# class CountryOfInterestInline(GenericTabularInline):
#     model = CountryOfInterest
#     ct_field = 'person_content_type'
#     ct_fk_field = 'person_id'
#
#
# class PoliticalInterestInline(GenericTabularInline):
#     model = PoliticalInterest
#     ct_field = 'person_content_type'
#     ct_fk_field = 'person_id'


@admin.register(*[
    Constituency,
    Party,
    WebLink,
    # CountryOfInterest,
    # PoliticalInterest,
])
class DefaultAdmin(admin.ModelAdmin):
    pass


@admin.register(Mp)
class MpAdmin(DefaultAdmin):
    inlines = [
        PersonalLinksInline,
        InterestInline,
        # PoliticalInterestInline,
        # CountryOfInterestInline,
    ]
