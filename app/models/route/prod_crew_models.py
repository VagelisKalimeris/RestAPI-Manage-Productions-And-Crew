from datetime import date
from enum import Enum

from pydantic import BaseModel


class SortCrewAvailabilityBy(str, Enum):
    """
    Purposed for GET request params validation.
    """
    highest_count = 'highest_count'
    lowest_count = 'lowest_count'


class CrewAvailabilityResult(BaseModel):
    message: str
    from_date: date
    to_date: date
    filtered_by_role: str | None
    data: dict
