from datetime import datetime

from api.schema.mini import MemberMiniSchema
from api.schema.types import ParliamentSchema, Url, field
from ninja import Schema
from repository.models.bill import BillStage
from repository.models.houses import HouseType

__all__ = [
    "BillFullSchema",
]


class BillType(ParliamentSchema):
    category: str = field("category.name")
    name: str
    description: str


class PublicationLink(Schema):
    title: str
    url: Url
    content_type: str


class Publication(ParliamentSchema):
    title: str
    date: datetime = field("display_date")
    type: str = field("publication_type.name")
    links: list[PublicationLink]


class Session(ParliamentSchema):
    name: str | None


class SponsorOrganisation(Schema):
    name: str
    url: Url


class Sponsor(Schema):
    id: int
    profile: MemberMiniSchema | None = field("member", default=None)
    organisation: SponsorOrganisation | None


class Stage(Schema):
    sittings: list[datetime]
    session: Session
    house: HouseType = field("house.name")
    latest_sitting: datetime | None

    @staticmethod
    def resolve_sittings(stage: BillStage):
        return stage.sittings.values_list("date", flat=True)

    @staticmethod
    def resolve_latest_sitting(stage: BillStage) -> datetime:
        return stage.sittings.order_by("-date").first().date


class BillFullSchema(ParliamentSchema):
    title: str
    description: str | None = field("summary", default=None)
    type: BillType = field("bill_type")
    last_update: datetime
    is_act: bool
    is_defeated: bool
    date_withdrawn: datetime | None = field("withdrawn_at", default=None)
    sponsors: list[Sponsor]
    publications: list[Publication]
    session_introduced: Session
    sessions: list[Session]
    current_stage: Stage | None
    stages: list[Stage]
