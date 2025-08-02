from datetime import datetime

from ninja import Schema

from api.schema.includes import MemberMiniSchema, OrganisationSchema
from api.schema.types import House, ParliamentSchema, Safe, Url, field
from repository.models.bill import BillStage

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


class Sponsor(Schema):
    id: int
    profile: MemberMiniSchema | None = field("member", default=None)
    organisation: OrganisationSchema | None


class Stage(Schema):
    session: Session
    house: Safe[House]
    description: str | None
    sittings: list[datetime]

    @staticmethod
    def resolve_sittings(stage: BillStage):
        return stage.sittings.values_list("date", flat=True)


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
