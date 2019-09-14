from typing import (
    Optional,
    List,
    Dict,
)

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from api import contract
from repository.models.people import GenericPersonOneToOneMixin

PHONE_NUMBER_REGION = 'GB'


class PersonalLinks(GenericPersonOneToOneMixin, models.Model):
    """Contact details and related web links. Telephony stuff."""
    phone_parliament = PhoneNumberField(
        null=True,
        help_text='National office phone number')
    phone_constituency = PhoneNumberField(
        null=True,
        help_text='Local office phone number')

    email = models.EmailField(null=True)

    wikipedia = models.CharField(
        null=True,
        max_length=64,
        help_text='Path section of a wikipedia url (e.g. \'John_Baron_(politician)\')')

    @classmethod
    def create(
            cls,
            person,
            email: Optional[str] = None,
            wikipedia: Optional[str] = None,
            phone_constituency: Optional[str] = None,
            phone_parliament: Optional[str] = None,
            weblinks: Optional[List[str]] = None,
    ) -> Optional['PersonalLinks']:
        if not (email or wikipedia or phone_constituency
                or phone_parliament or weblinks):
            return None

        if phone_parliament:
            try:
                phone_parliament = PhoneNumber.from_string(
                    phone_parliament, region=PHONE_NUMBER_REGION)
            except (NumberParseException, ValueError):
                phone_parliament = None
        if phone_constituency:
            try:
                phone_constituency = PhoneNumber.from_string(
                    phone_constituency, region=PHONE_NUMBER_REGION)
            except (NumberParseException, ValueError):
                phone_constituency = None

        links = cls(
            person=person,
            email=email,
            wikipedia=wikipedia,
            phone_constituency=phone_constituency,
            phone_parliament=phone_parliament)
        links.save()

        if weblinks:
            for url in weblinks:
                WebLink.objects.create(
                    links=links,
                    url=url).save()
        return links

    @property
    def phone_numbers(self) -> Dict:
        obj = {}
        if self.phone_constituency:
            obj[contract.PHONE_CONSTITUENCY] = self.phone_constituency.as_national.replace(' ', '')

        if self.phone_parliament:
            obj[contract.PHONE_PARLIAMENT] = self.phone_parliament.as_national.replace(' ', '')

        return obj

    def to_json(self):
        json = {
            contract.EMAIL: self.email,
            contract.WIKIPEDIA: self.wikipedia,
            contract.PHONE: self.phone_numbers,
            contract.WEBLINKS: [
                x.url for x in WebLink.objects.filter(links=self)
            ]
        }
        for key, value in json.items():
            if not value:
                del json[key]
        return json

    class Meta:
        verbose_name_plural = 'Personal links'

    def __str__(self):
        return f'{self.person}'


class WebLink(models.Model):
    """Social media, personal sites, etc"""
    links = models.ForeignKey(
        PersonalLinks,
        on_delete=models.CASCADE,
        related_name='weblinks',
        related_query_name='weblink')
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url
