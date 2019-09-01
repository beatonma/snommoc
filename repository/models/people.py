import logging
from typing import (
    Optional,
    Type,
    List,
)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .util.generics import GetSubclassesMixin

UNKNOWN_ID = 0
NAME_MAX_LENGTH = 72

log = logging.getLogger(__name__)


class Person(GetSubclassesMixin, models.Model):
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='Canonical name for this person.')

    given_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='First name',
        null=True)

    family_name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        help_text='Last name',
        null=True)

    @property
    def filter_query(self):
        """
        Workaround due to use of abstraction and GenericForeignKey:
        We can't filter by SomeModel.objects.filter(person=some_person)
        so use SomeModel.objects.filter(**some_person.filter_query) instead.
        """
        return {
            'person_id': self.id,
            'person_content_type': ContentType.objects.get_for_model(self)
        }

    def filtered(
            self,
            model_class: Type['GenericPersonForeignKeyMixin'],
            **kwargs
    ):
        """Convenience method for `filter_query`"""
        return model_class.objects.filter(**self.filter_query, **kwargs)

    def get(
            self,
            model_class: Type['GenericPersonForeignKeyMixin'],
            **kwargs
    ):
        return model_class.objects.get(**self.filter_query, **kwargs)

    def get_or_create(
            self,
            model_class: Type['GenericPersonForeignKeyMixin'],
            **kwargs
    ):
        return model_class.objects.get_or_create(**self.filter_query, **kwargs)


class GenericPersonForeignKeyMixin(models.Model):
    person_content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=Person.get_subclasses,
        on_delete=models.CASCADE,
        null=True)
    person_id = models.PositiveIntegerField(null=True)
    person = GenericForeignKey('person_content_type', 'person_id')


class NameAlias(GenericPersonForeignKeyMixin, models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH)

    @property
    def canonical(self) -> Optional[str]:
        return self.person.name if self.person else None

    @classmethod
    def create(cls, person, names: List[str]) -> List['NameAlias']:
        aliases = []
        for name in names:
            alias = cls.objects.create(person=person, name=name)
            alias.save()
            aliases.append(alias)
        return aliases


class SuggestedAlias(GenericPersonForeignKeyMixin, models.Model):
    class Meta:
        permissions = [
            (
                'confirm_name_alias',
                'Can confirm that one name can be handled as an alias of another.'
            )
        ]

    alias = models.ForeignKey(NameAlias, on_delete=models.CASCADE)

    def approve_as_alias(self):
        """Confirm the NamAlias matches the PersonID"""
        self.alias.person = self.person
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
        original_name = self.person.name
        self.person.name = self.alias.name
        self.alias.name = original_name

        # Associate PersonID with NameAlias
        self.alias.person = self.person
        self.alias.save()
        self.person.save()

        # Consume the suggestion
        self.delete()
