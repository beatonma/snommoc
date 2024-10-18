from typing import List

from ninja import Schema

from .types import EmailAddress, PhoneNumber, WebAddress, alias


class PhysicalAddressSchema(Schema):
    description: str | None = None
    address: str | None = None
    postcode: str | None = None
    phone: PhoneNumber | None
    fax: PhoneNumber | None
    email: EmailAddress | None = None


class WebAddressSchema(Schema):
    url: WebAddress
    description: str | None


class AddressSchema(Schema):
    physical: List[PhysicalAddressSchema] = alias("physicaladdress_set")
    web: List[WebAddressSchema] = alias("webaddress_set")
