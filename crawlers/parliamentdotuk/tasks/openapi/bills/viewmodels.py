"""Viewmodels for parsing responses from Bill OpenAPI endpoints."""

import enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from crawlers.parliamentdotuk.tasks.util.coercion import coerce_to_datetime


@enum.unique
class House(enum.Enum):
    """Definition from https://bills-api.parliament.uk/index.html"""

    All = enum.auto()
    Commons = enum.auto()
    Lords = enum.auto()
    Unassigned = enum.auto()


@enum.unique
class BillTypeCategory(enum.Enum):
    """Definition from https://bills-api.parliament.uk/index.html"""

    Public = enum.auto()
    Private = enum.auto()
    Hybrid = enum.auto()


class BillType:
    """Schema definition: BillType from https://bills-api.parliament.uk/index.html"""

    id: int
    category: BillTypeCategory
    name: str
    description: str

    def __init__(
        self,
        id: int,
        category: str,
        name: str,
        description: str,
    ):
        self.id = id
        self.category = BillTypeCategory[category]
        self.name = name
        self.description = description


class BillStageType:
    """Schema definition: BillStage from https://bills-api.parliament.uk/index.html"""

    id: int
    name: str
    house: House

    def __init__(self, id: int, name: str, house: str):
        print(id, name, house)
        self.id = id
        self.name = name
        self.house = House[house]


@dataclass
class BillStageSitting:
    """Schema definition: BillStageSitting from https://bills-api.parliament.uk/index.html"""

    id: int
    stageId: int
    billStageId: int
    billId: int
    date: Optional[datetime]

    def __init__(
        self,
        id: int,
        stageId: int,
        billStageId: int,
        billId: int,
        date: Optional[str],
    ):
        self.id = id
        self.stageId = stageId
        self.billStageId = billStageId
        self.billId = billId
        self.date = coerce_to_datetime(date)


class StageSummary:
    """Schema definition: StageSummary from https://bills-api.parliament.uk/index.html

    :param id: Unique identifier for this StageSummary.
    :param stageId: ID for related BillStageType.
    :param sessionId: ID for related ParliamentarySession.
    """

    id: int
    stageId: int
    sessionId: int
    description: Optional[str]
    abbreviation: Optional[str]
    house: House
    stageSittings: List[BillStageSitting]
    sortOrder: int

    def __init__(
        self,
        id: int,
        stageId: int,
        sessionId: int,
        description: Optional[str],
        abbreviation: Optional[str],
        house: str,
        stageSittings: List[dict],
        sortOrder: int,
    ):
        self.id = id
        self.stageId = stageId
        self.sessionId = sessionId
        self.description = description
        self.abbreviation = abbreviation
        self.house = House[house]
        self.stageSittings = [BillStageSitting(**x) for x in stageSittings]
        self.sortOrder = sortOrder


class BillSummary:
    """Schema definition: BillSummary from https://bills-api.parliament.uk/index.html"""

    billId: int
    shortTitle: str
    currentHouse: House
    originatingHouse: House
    lastUpdate: datetime
    billWithdrawn: Optional[datetime]
    isDefeated: bool
    billTypeId: int
    introducedSessionId: int
    includedSessionIds: List[int]
    isAct: bool
    currentStage: StageSummary

    def __init__(
        self,
        billId: int,
        shortTitle: str,
        currentHouse: str,
        originatingHouse: str,
        lastUpdate: str,
        billWithdrawn: Optional[datetime],
        isDefeated: bool,
        billTypeId: int,
        introducedSessionId: int,
        includedSessionIds: List[int],
        isAct: bool,
        currentStage: dict,
    ):
        self.billId = billId
        self.shortTitle = shortTitle
        self.currentHouse = House[currentHouse]
        self.originatingHouse = House[originatingHouse]
        self.lastUpdate = coerce_to_datetime(lastUpdate)
        self.billWithdrawn = coerce_to_datetime(billWithdrawn)
        self.isDefeated = isDefeated
        self.billTypeId = billTypeId
        self.introducedSessionId = introducedSessionId
        self.includedSessionIds = includedSessionIds
        self.isAct = isAct
        self.currentStage = StageSummary(**currentStage) if currentStage else None


@dataclass
class BillAgent:
    """Schema definition: BillAgent from https://bills-api.parliament.uk/index.html"""

    name: Optional[str]
    address: Optional[str]
    phoneNo: Optional[str]
    email: Optional[str]
    website: Optional[str]


class Member:
    """Schema definition: Member from https://bills-api.parliament.uk/index.html"""

    memberId: int
    name: Optional[str]
    party: Optional[str]
    partyColor: Optional[str]
    house: House
    memberPhoto: Optional[str]
    memberPage: Optional[str]
    memberFrom: Optional[str]

    def __init__(
        self,
        memberId: int,
        name: Optional[str],
        party: Optional[str],
        partyColour: Optional[str],
        house: str,
        memberPhoto: Optional[str],
        memberPage: Optional[str],
        memberFrom: Optional[str],
    ):
        self.memberId = memberId
        self.name = name
        self.party = party
        self.partyColor = partyColour
        self.house = House[house]
        self.memberPhoto = memberPhoto
        self.memberPage = memberPage
        self.memberFrom = memberFrom


@dataclass
class Organisation:
    """Schema definition: Organisation from https://bills-api.parliament.uk/index.html"""

    name: Optional[str]
    url: Optional[str]


@dataclass
class Promoter:
    """Schema definition: Promoter from https://bills-api.parliament.uk/index.html"""

    organisationName: Optional[str]
    organisationUrl: Optional[str]


class Sponsor:
    """Schema definition: Sponsor from https://bills-api.parliament.uk/index.html"""

    member: Optional[Member]
    organisation: Optional[Organisation]
    sortOrder: int

    def __init__(
        self,
        member: Optional[dict],
        organisation: Optional[dict],
        sortOrder: int,
    ):
        self.member = Member(**member) if member else None
        self.organisation = Organisation(**organisation) if organisation else None
        self.sortOrder = sortOrder


class Bill(BillSummary):
    """Schema definition: Bill from https://bills-api.parliament.uk/index.html"""

    longTitle: Optional[str]
    summary: Optional[str]
    sponsors: List[Sponsor]
    promoters: List[Promoter]
    petitioningPeriod: Optional[str]
    petitionInformation: Optional[str]
    agent: BillAgent

    def __init__(
        self,
        billId: int,
        shortTitle: Optional[str],
        currentHouse: str,
        originatingHouse: str,
        lastUpdate: str,
        billWithdrawn: Optional[str],
        isDefeated: bool,
        billTypeId: int,
        introducedSessionId: int,
        includedSessionIds: List[int],
        isAct: bool,
        currentStage: dict,
        longTitle: Optional[str],
        summary: Optional[str],
        sponsors: List[dict],
        promoters: List[dict],
        petitioningPeriod: Optional[str],
        petitionInformation: Optional[str],
        agent: dict,
    ):
        super().__init__(
            billId=billId,
            shortTitle=shortTitle,
            currentHouse=currentHouse,
            originatingHouse=originatingHouse,
            lastUpdate=lastUpdate,
            billWithdrawn=billWithdrawn,
            isDefeated=isDefeated,
            billTypeId=billTypeId,
            introducedSessionId=introducedSessionId,
            includedSessionIds=includedSessionIds,
            isAct=isAct,
            currentStage=currentStage,
        )
        self.longTitle = longTitle
        self.summary = summary
        self.sponsors = [Sponsor(**x) for x in sponsors]
        self.promoters = [Promoter(**x) for x in promoters]
        self.petitioningPeriod = petitioningPeriod
        self.petitionInformation = petitionInformation
        self.agent = BillAgent(**agent) if agent else None
