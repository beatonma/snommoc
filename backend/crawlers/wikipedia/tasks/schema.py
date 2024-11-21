from pydantic import BaseModel as Schema
from pydantic import Field


class Page(Schema):
    pageid: int
    title: str


class Normalized(Schema):
    original: str = Field(validation_alias="from")
    to: str


class Query[T: Page](Schema):
    normalized: list[Normalized] | None = Field(default=None)
    pages: dict[str, T]


class BatchResponse[T: Page](Schema):
    batchcomplete: str
    query: Query[T]


class Image(Schema):
    source: str
    width: int
    height: int


class Images(Page):
    thumbnail: Image | None = Field(default=None)
    original: Image | None = Field(default=None)


class ImagesBatchResponse(BatchResponse[Images]):
    pass
