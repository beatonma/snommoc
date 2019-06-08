from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from phonenumbers import NumberParseException

from repository.models import GenericPersonForeignKeyMixin, Optional, List

PHONE_NUMBER_REGION = 'GB'


class PersonalLinks(GenericPersonForeignKeyMixin, models.Model):
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
    ):
        if phone_parliament:
            try:
                phone_parliament = PhoneNumber.from_string(
                    phone_parliament, region=PHONE_NUMBER_REGION)
            except NumberParseException:
                phone_parliament = None
        if phone_constituency:
            try:
                phone_constituency = PhoneNumber.from_string(
                    phone_constituency, region=PHONE_NUMBER_REGION)
            except NumberParseException:
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


class WebLink(models.Model):
    """Twitter, Facebook, personal sites, etc"""
    links = models.ForeignKey(
        PersonalLinks,
        on_delete=models.CASCADE,
        related_name='weblinks',
        related_query_name='weblink')
    url = models.URLField(unique=True)
