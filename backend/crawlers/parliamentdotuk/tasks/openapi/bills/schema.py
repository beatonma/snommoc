"""Viewmodels for parsing responses from Bill OpenAPI endpoints."""

import enum
from typing import Annotated

from pydantic import BaseModel as Schema
from pydantic import BeforeValidator, Field

from crawlers.parliamentdotuk.tasks.types import (
    Color,
    DateTimeOrNone,
    PersonName,
    PhoneNumber,
    SafeHtmlOrNone,
    StringOrNone,
    field,
)


@enum.unique
class House(enum.StrEnum):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-House"""

    All = "All"
    Commons = "Commons"
    Lords = "Lords"
    Unassigned = "Unassigned"


@enum.unique
class BillTypeCategory(enum.StrEnum):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillTypeCategory"""

    Public = "Public"
    Private = "Private"
    Hybrid = "Hybrid"


class BillType(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillType#model-BillType"""

    id: int
    category: BillTypeCategory
    name: str
    description: Annotated[
        SafeHtmlOrNone,
        BeforeValidator(lambda x: x.replace("<div>", "<br><div>") if x else None),
    ]  # Insert <br> to keep block layout behaviour when <div> is stripped.


class BillStageType(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillStage"""

    id: int
    name: str
    house: House


class BillStageSitting(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillStageSitting"""

    id: int
    stageId: int
    bill_stage_id: int = field("billStageId")
    bill_id: int = field("billId")
    date: DateTimeOrNone


class StageSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.h#model-StageSummarytml

    :param id: Unique identifier for this StageSummary.
    :param stage_id: ID for related BillStageType.
    :param session_id: ID for related ParliamentarySession.
    """

    id: int
    stage_id: int = field("stageId")
    session_id: int = field("sessionId")
    description: StringOrNone
    abbreviation: StringOrNone
    house: House
    stage_sittings: list[BillStageSitting] = field("stageSittings")
    sort_order: int = field("sortOrder")


class BillAgent(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillAgent"""

    name: StringOrNone
    address: StringOrNone
    phone: PhoneNumber = field("phoneNo")
    email: StringOrNone
    website: StringOrNone


class Member(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Member"""

    member_id: int = field("memberId")
    name: PersonName
    party: StringOrNone
    party_color: Color = Field(alias="partyColour")
    house: House
    member_photo: StringOrNone = field("memberPhoto")
    member_page: StringOrNone = field("memberPage")
    member_from: StringOrNone = field("memberFrom")


class Organisation(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Organisation"""

    name: StringOrNone
    url: StringOrNone


class Promoter(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Promoter"""

    organisation_name: StringOrNone = field("organisationName")
    organisation_url: StringOrNone = field("organisationUrl")


class Sponsor(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Sponsor"""

    member: Member | None
    organisation: Organisation | None
    sort_order: int = field("sortOrder")


class BillPublicationLink(Schema):
    id: int
    title: str
    url: str
    content_type: str = field("contentType")


class BillPublicationType(Schema):
    id: int
    name: str
    description: StringOrNone


class BillPublication(Schema):
    id: int
    house: House
    title: str
    display_date: DateTimeOrNone = field("displayDate")
    publication_type: BillPublicationType = field("publicationType")
    links: list[BillPublicationLink]


class BillSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillSummary"""

    bill_id: int = field("billId")
    short_title: str = field("shortTitle")
    current_house: House = field("currentHouse")
    originating_house: House = field("originatingHouse")
    last_update: DateTimeOrNone = field("lastUpdate")
    bill_withdrawn: DateTimeOrNone = field("billWithdrawn")
    is_defeated: bool = field("isDefeated")
    bill_type_id: int = field("billTypeId")
    introduced_session_id: int = field("introducedSessionId")
    included_session_ids: list[int] = field("includedSessionIds")
    is_act: bool = field("isAct")
    current_stage: StageSummary | None = field("currentStage")


class Bill(BillSummary, Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Bill"""

    long_title: StringOrNone = field("longTitle")
    summary: SafeHtmlOrNone
    sponsors: list[Sponsor]
    promoters: list[Promoter]
    petitioning_period: StringOrNone = field("petitioningPeriod")
    petition_information: StringOrNone = field("petitionInformation")
    agent: BillAgent | None
