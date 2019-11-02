from typing import (
    List,
    Optional,
)

from django.db import models

from repository.models import (
    Party,
    Constituency,
)
from repository.models.contact_details import Links
from repository.models.interests import (
    Interest,
    INTEREST_CATEGORY_COUNTRY,
    INTEREST_CATEGORY_GENERIC,
)
from repository.models.mixins import (
    TheyWorkForYouMixin,
    PeriodMixin,
    ParliamentDotUkMixin,
)
from repository.models.person import Person
from repository.models.util.queryset import get_or_none


class Mp(ParliamentDotUkMixin, TheyWorkForYouMixin, PeriodMixin, models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='people',
        related_query_name='person'
    )

    party = models.ForeignKey(
        Party,
        on_delete=models.CASCADE,
        related_name='parties',
        related_query_name='party',
        null=True)

    @property
    def links(self):
        return self.person.links

    @property
    def interests(self):
        return self.person.interests.all()

    @property
    def countries_of_interest(self):
        return self.person.interests.filter(category=INTEREST_CATEGORY_COUNTRY)

    @property
    def generic_interests(self):
        return self.person.interests.filter(category=INTEREST_CATEGORY_GENERIC)

    @classmethod
    def create(
            cls,
            name: str,
            puk: int,
            given_name: Optional[str] = None,
            family_name: Optional[str] = None,
            aliases: Optional[List[str]] = None,
            twfy: Optional[int] = None,
            party: Optional[str] = None,
            constituency: Optional[str] = None,
            email: Optional[str] = None,
            phone_constituency: Optional[str] = None,
            phone_parliamentary: Optional[str] = None,
            weblinks: Optional[List[str]] = None,
            interests_political: Optional[List[str]] = None,
            interests_countries: Optional[List[str]] = None,
            wikipedia_path: Optional[str] = None
    ) -> 'Mp':
        person, _ = Person.objects.update_or_create(
            name=name,
            defaults={
                'name': name,
                'given_name': given_name,
                'family_name': family_name,
            })

        mp = cls(
            # name=name, given_name=given_name, family_name=family_name,
            person=person,
            parliamentdotuk=puk,
            theyworkforyou=twfy,
        )
        if party:
            mp.party = get_or_none(Party, name=party)
        if constituency:
            mp.constituency = get_or_none(Constituency, name=constituency)

        mp.save()

        # if aliases:
        #     NameAlias.create(mp, aliases)

        Links.create(
            person,
            email=email,
            phone_constituency=phone_constituency,
            phone_parliament=phone_parliamentary,
            weblinks=weblinks,
            wikipedia=wikipedia_path
        )

        if interests_political:
            Interest.create(person, interests_political)

        if interests_countries:
            Interest.create_countries(person, interests_countries)

        return mp

    # @property
    # def aliases(self) -> List[str]:
    #     return [a.name for a in self.filtered(NameAlias)]

    # def merge(
    #         self,
    #         other: 'Mp',
    #         delete_other: bool = False
    # ) -> Tuple['Mp', Optional['SuggestedAlias']]:
    #     """
    #     TODO UPDATE TO COMBINE ALL FIELDS
    #
    #     Merge other into self. If names are different then a SuggestedAlias will
    #     be created and returned along with the merged PersonID.
    #     """
    #     self.parliamentdotuk = self.parliamentdotuk or other.parliamentdotuk
    #     self.theyworkforyou = self.theyworkforyou or other.theyworkforyou
    #     suggestion = None
    #     if self.name != other.name:
    #         alias, _ = NameAlias.objects.get_or_create(name=other.name)
    #         suggestion, _ = SuggestedAlias.objects.get_or_create(
    #             alias=alias,
    #             **self.filter_query)
    #
    #     if delete_other:
    #         other.delete()
    #
    #     return self, suggestion

    # @property
    # def political_interests(self):
    #     return [item.description for item in self.filtered(PoliticalInterest)]
    #
    # @property
    # def countries_of_interest(self):
    #     return [item.country for item in self.filtered(CountryOfInterest)]

    # @property
    # def links(self) -> Optional[Links]:
    #     try:
    #         return self.get(Links)
    #     except Links.DoesNotExist:
    #         return None

    class Meta:
        verbose_name_plural = 'MPs'
        verbose_name = 'MP'

    def __str__(self):
        return self.person.name
