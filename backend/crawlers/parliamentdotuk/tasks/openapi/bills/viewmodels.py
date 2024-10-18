"""Viewmodels for parsing responses from Bill OpenAPI endpoints."""

import enum
from typing import List

from crawlers.parliamentdotuk.tasks.types import CoercedDateTime
from pydantic import BaseModel as Schema
from pydantic import Field


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
    description: str


class BillStageType(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillStage"""

    id: int
    name: str
    house: House


class BillStageSitting(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillStageSitting"""

    id: int
    stageId: int
    billStageId: int
    billId: int
    date: CoercedDateTime | None


class StageSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.h#model-StageSummarytml

    :param id: Unique identifier for this StageSummary.
    :param stageId: ID for related BillStageType.
    :param sessionId: ID for related ParliamentarySession.
    """

    id: int
    stageId: int
    sessionId: int
    description: str | None
    abbreviation: str | None
    house: House
    stageSittings: List[BillStageSitting]
    sortOrder: int


class BillAgent(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillAgent"""

    name: str | None
    address: str | None
    phoneNo: str | None
    email: str | None
    website: str | None


class Member(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Member"""

    memberId: int
    name: str | None
    party: str | None
    partyColor: str | None = Field(alias="partyColour")
    house: House
    memberPhoto: str | None
    memberPage: str | None
    memberFrom: str | None


class Organisation(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Organisation"""

    name: str | None
    url: str | None


class Promoter(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Promoter"""

    organisationName: str | None
    organisationUrl: str | None


class Sponsor(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Sponsor"""

    member: Member | None
    organisation: Organisation | None
    sortOrder: int


class BillPublicationLink(Schema):
    id: int
    title: str
    url: str
    contentType: str


class BillPublicationType(Schema):
    id: int
    name: str
    description: str


class BillPublication(Schema):
    id: int
    house: House
    title: str
    displayDate: CoercedDateTime
    publicationType: BillPublicationType
    links: List[BillPublicationLink]


class BillSummary(Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-BillSummary"""

    billId: int
    shortTitle: str
    currentHouse: House
    originatingHouse: House
    lastUpdate: CoercedDateTime
    billWithdrawn: CoercedDateTime | None
    isDefeated: bool
    billTypeId: int
    introducedSessionId: int
    includedSessionIds: List[int]
    isAct: bool
    currentStage: StageSummary | None


class Bill(BillSummary, Schema):
    """Schema definition: https://bills-api.parliament.uk/index.html#model-Bill"""

    longTitle: str | None
    summary: str | None
    sponsors: List[Sponsor]
    promoters: List[Promoter]
    petitioningPeriod: str | None
    petitionInformation: str | None
    agent: BillAgent | None
