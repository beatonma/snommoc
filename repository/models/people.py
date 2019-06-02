import logging
from typing import List, Optional, Tuple

from django.db import models

UNKNOWN_ID = 0
NAME_MAX_LENGTH = 128

log = logging.getLogger(__name__)


class PersonID(models.Model):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='Canonical name for this person.')
    parliamentdotuk = models.PositiveIntegerField(
        unique=True,
        null=True,
        help_text='ID used on parliament.uk website')
    theyworkforyou = models.PositiveIntegerField(
        unique=True,
        null=True,
        help_text='ID used on theyworkforyou.com')

    @classmethod
    def create(cls, name: str, puk: Optional[int] = None, twfy: Optional[int] = None):
        return cls(name=name, parliamentdotuk=puk, theyworkforyou=twfy)

    @property
    def aliases(self) -> List[str]:
        return [alias.name for alias in self.also_known_as.all()]

    def merge(
            self,
            other: 'PersonID',
            delete_other: bool = False
    ) -> Tuple['PersonID', Optional['SuggestedAlias']]:
        """
        Merge other into self. If names are different then a SuggestedAlias will
        be created and returned along with the merged PersonID.
        """
        self.parliamentdotuk = self.parliamentdotuk or other.parliamentdotuk
        self.theyworkforyou = self.theyworkforyou or other.theyworkforyou
        suggestion = None
        if self.name != other.name:
            alias, _ = NameAlias.objects.get_or_create(name=other.name)
            suggestion, _ = SuggestedAlias.objects.get_or_create(personID=self, alias=alias)

        if delete_other:
            other.delete()

        return self, suggestion


class NameAlias(models.Model):
    """Use one of the ID fields to find aliases for a name."""

    name = models.CharField(max_length=NAME_MAX_LENGTH)
    personID = models.ForeignKey(
        PersonID,
        on_delete=models.CASCADE,
        related_name='also_known_as',
        blank=True,
        null=True)

    @property
    def canonical(self) -> Optional[str]:
        return self.personID.name if self.personID else None


class SuggestedAlias(models.Model):
    class Meta:
        permissions = [
            (
                'confirm_name_alias',
                'Can confirm that one name can be handled as an alias of another.'
            )
        ]

    personID = models.ForeignKey(PersonID, on_delete=models.CASCADE)
    alias = models.ForeignKey(NameAlias, on_delete=models.CASCADE)

    def approve_as_alias(self):
        """Confirm the NamAlias matches the PersonID"""
        self.alias.personID = self.personID
        self.alias.save()

        # Consume the suggestion
        self.delete()

    def approve_as_canonical(self):
        """
        Confirm the NamAlias matches the PersonID, but swap the names
        so that the alias becomes canonical and the old canonical becomes
        an alias.
        """
        # Swap names
        original_name = self.personID.name
        self.personID.name = self.alias.name
        self.alias.name = original_name

        # Associate PersonID with NameAlias
        self.alias.personID = self.personID
        self.alias.save()
        self.personID.save()

        # Consume the suggestion
        self.delete()
