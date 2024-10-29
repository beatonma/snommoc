from crawlers.parliamentdotuk.tasks.types import field
from pydantic import BaseModel as Schema
from pydantic import model_validator

from .constituency import Constituency
from .division import CommonsDivision, CommonsDivisionItem, Vote, VoteType
from .election_results import ElectionCandidate, ElectionResult, ElectionResultDetail


class Page[T: Schema](Schema):
    items: list[T] = field("items")
    items_per_page: int = field("itemsPerPage")
    page: int
    start_index: int = field("startIndex")  # index of first item on the page
    total_results: int = field("totalResults")
    prev_page_url: str | None = field("prev", default=None)
    next_page_url: str | None = field("next", default=None)

    @model_validator(mode="before")
    def unwrap(cls, obj):
        return obj["result"]


class Item[T: Schema](Schema):
    """
    Example:
        https://lda.data.parliament.uk/commonsdivisions/id/1720066.json
    """

    data: T = field("result.primaryTopic")
