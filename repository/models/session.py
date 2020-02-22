"""

"""

import logging

from repository.models.mixins import (
    PeriodMixin,
    BaseModel,
    ParliamentDotUkMixin,
)

log = logging.getLogger(__name__)


class ParliamentarySession(ParliamentDotUkMixin, PeriodMixin, BaseModel):
    """A legislative session, usually lasting about a year."""
    pass
