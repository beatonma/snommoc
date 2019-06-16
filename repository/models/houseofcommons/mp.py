from typing import (
    Optional,
    List,
    Tuple,
)

from django.db import models

from api import contract
from repository.models import (
    Person,
    NameAlias,
    SuggestedAlias,
    Party,
    Constituency,
)
from repository.models.contact_details import PersonalLinks
from repository.models.interests import (
    CountryOfInterest,
    PoliticalInterest,
)
from repository.models.util.models import get_or_none


class Mp(Person):
    parliamentdotuk = models.PositiveIntegerField(
        unique=True,
        null=True,
        help_text='ID used on parliament.uk website')
    theyworkforyou = models.PositiveIntegerField(
        unique=True,
        null=True,
        help_text='ID used on theyworkforyou.com')

    party = models.ForeignKey(
        Party,
        on_delete=models.DO_NOTHING,
        related_name='parties',
        related_query_name='party',
        null=True)

    @classmethod
    def create(
            cls,
            name: str,
            aliases: Optional[List[str]] = None,
            puk: Optional[int] = None,
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
        mp = cls(name=name, parliamentdotuk=puk, theyworkforyou=twfy)
        if party:
            mp.party = get_or_none(Party, name=party)
        if constituency:
            mp.constituency = get_or_none(Constituency, name=constituency)

        mp.save()

        if aliases:
            NameAlias.create(mp, aliases)

        PersonalLinks.create(
            mp,
            email=email,
            phone_constituency=phone_constituency,
            phone_parliament=phone_parliamentary,
            weblinks=weblinks,
            wikipedia=wikipedia_path
        )

        if interests_political:
            PoliticalInterest.create(mp, interests_political)

        if interests_countries:
            CountryOfInterest.create(mp, interests_countries)

        return mp

    @property
    def aliases(self) -> List[str]:
        return [a.name for a in self.filtered(NameAlias)]

    def merge(
            self,
            other: 'Mp',
            delete_other: bool = False
    ) -> Tuple['Mp', Optional['SuggestedAlias']]:
        """
        TODO UPDATE TO COMBINE ALL FIELDS

        Merge other into self. If names are different then a SuggestedAlias will
        be created and returned along with the merged PersonID.
        """
        self.parliamentdotuk = self.parliamentdotuk or other.parliamentdotuk
        self.theyworkforyou = self.theyworkforyou or other.theyworkforyou
        suggestion = None
        if self.name != other.name:
            alias, _ = NameAlias.objects.get_or_create(name=other.name)
            suggestion, _ = SuggestedAlias.objects.get_or_create(
                alias=alias,
                **self.filter_query)

        if delete_other:
            other.delete()

        return self, suggestion

    @property
    def political_interests(self):
        return [item.description for item in self.filtered(PoliticalInterest)]

    @property
    def countries_of_interest(self):
        return [item.country for item in self.filtered(CountryOfInterest)]

    @property
    def links(self) -> Optional[PersonalLinks]:
        try:
            return self.get(PersonalLinks)
        except PersonalLinks.DoesNotExist:
            return None

    def to_json(self):
        json = {
            contract.NAME: self.name,
            contract.ALIASES: self.aliases,
            contract.THEYWORKFORYOU_ID: self.theyworkforyou,
            contract.PARLIAMENTDOTUK_ID: self.parliamentdotuk,
            contract.PARTY: self.party.name,
            contract.CONSTITUENCY: self.constituency.name,
            contract.INTERESTS: {
                contract.INTERESTS_POLITICAL: self.political_interests,
                contract.INTERESTS_COUNTRIES: self.countries_of_interest,
            },
        }
        links = self.links
        if links:
            json[contract.PERSONAL_LINKS] = links.to_json()

        return json
