"""Viewmodels for parsing responses from Bill OpenAPI endpoints."""

import enum
from typing import Annotated

from crawlers.parliamentdotuk.tasks.types import (
    CoercedColor,
    CoercedDateTime,
    CoercedPhoneNumber,
    CoercedStr,
    PersonName,
    SanitizedHtmlStr,
    field,
)
from pydantic import BaseModel as Schema
from pydantic import BeforeValidator, Field


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
        SanitizedHtmlStr,
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
    date: CoercedDateTime


class StageSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.h#model-StageSummarytml

    :param id: Unique identifier for this StageSummary.
    :param stage_id: ID for related BillStageType.
    :param session_id: ID for related ParliamentarySession.
    """

    id: int
    stage_id: int = field("stageId")
    session_id: int = field("sessionId")
    description: CoercedStr
    abbreviation: CoercedStr
    house: House
    stage_sittings: list[BillStageSitting] = field("stageSittings")
    sort_order: int = field("sortOrder")


class BillAgent(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillAgent"""

    name: CoercedStr
    address: CoercedStr
    phone: CoercedPhoneNumber = field("phoneNo")
    email: CoercedStr
    website: CoercedStr


class Member(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Member"""

    member_id: int = field("memberId")
    name: PersonName
    party: CoercedStr
    party_color: CoercedColor = Field(alias="partyColour")
    house: House
    member_photo: CoercedStr = field("memberPhoto")
    member_page: CoercedStr = field("memberPage")
    member_from: CoercedStr = field("memberFrom")


class Organisation(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Organisation"""

    name: CoercedStr
    url: CoercedStr


class Promoter(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Promoter"""

    organisation_name: CoercedStr = field("organisationName")
    organisation_url: CoercedStr = field("organisationUrl")


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
    description: str


class BillPublication(Schema):
    id: int
    house: House
    title: str
    display_date: CoercedDateTime = field("displayDate")
    publication_type: BillPublicationType = field("publicationType")
    links: list[BillPublicationLink]


class BillSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillSummary"""

    bill_id: int = field("billId")
    short_title: str = field("shortTitle")
    current_house: House = field("currentHouse")
    originating_house: House = field("originatingHouse")
    last_update: CoercedDateTime = field("lastUpdate")
    bill_withdrawn: CoercedDateTime = field("billWithdrawn")
    is_defeated: bool = field("isDefeated")
    bill_type_id: int = field("billTypeId")
    introduced_session_id: int = field("introducedSessionId")
    included_session_ids: list[int] = field("includedSessionIds")
    is_act: bool = field("isAct")
    current_stage: StageSummary | None = field("currentStage")


class Bill(BillSummary, Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Bill"""

    long_title: CoercedStr = field("longTitle")
    summary: SanitizedHtmlStr
    sponsors: list[Sponsor]
    promoters: list[Promoter]
    petitioning_period: CoercedStr = field("petitioningPeriod")
    petition_information: CoercedStr = field("petitionInformation")
    agent: BillAgent | None
