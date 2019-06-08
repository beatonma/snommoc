from typing import (
    Optional,
    List,
    Tuple,
)

from django.db import models

from repository.models import (
    Person,
    NameAlias,
    SuggestedAlias,
    Party
)
from repository.models.contact_details import PersonalLinks
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
            wikipedia_path: Optional[str] = None,
            save: bool = False
    ) -> 'Mp':
        # return cls(name=name, parliamentdotuk=puk, theyworkforyou=twfy)
        mp = cls(name=name, parliamentdotuk=puk, theyworkforyou=twfy)
        if party:
            mp.party = get_or_none(Party, name=party)
        if constituency:
            mp.constituency = get_or_none('Constituency', name=constituency)

        links = PersonalLinks.create(
            mp,
            email=email,
            phone_constituency=phone_constituency,
            phone_parliament=phone_parliamentary,
            weblinks=weblinks,
            wikipedia=wikipedia_path
        )

        if save:
            mp.save()
        return mp

    @property
    def aliases(self) -> List[str]:
        return [a.name for a in NameAlias.objects.filter(**self.filter_query)]

    def merge(
            self,
            other: 'Mp',
            delete_other: bool = False
    ) -> Tuple['Mp', Optional['SuggestedAlias']]:
        """
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
