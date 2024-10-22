from pydantic import BaseModel as Schema
from pydantic import Field, model_validator

from .constituency import Constituency
from .division import CommonsDivision, CommonsDivisionItem, Vote, VoteType
from .election_results import ElectionCandidate, ElectionResult, ElectionResultDetail


class Page[T: Schema](Schema):
    items: list[T] = Field(validation_alias="items")
    items_per_page: int = Field(validation_alias="itemsPerPage")
    page: int
    start_index: int = Field(
        validation_alias="startIndex"
    )  # index of first item on the page
    total_results: int = Field(validation_alias="totalResults")
    prev_page_url: str | None = Field(default=None, validation_alias="prev")
    next_page_url: str | None = Field(default=None, validation_alias="next")

    @model_validator(mode="before")
    @classmethod
    def unwrap(cls, obj):
        return obj["result"]


class Item[T: Schema](Schema):
    """
    Example:
        https://lda.data.parliament.uk/commonsdivisions/id/1720066.json
    """

    data: T = Field(validation_alias="primaryTopic")

    @model_validator(mode="before")
    @classmethod
    def unwrap(cls, obj):
        return obj["result"]
