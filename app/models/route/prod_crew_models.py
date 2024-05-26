from datetime import date
from enum import Enum


class SortCrewAvailabilityBy(str, Enum):
    """
    Purposed for GET request params validation.
    """
    highest_count = 'highest_count'
    lowest_count = 'lowest_count'


class CrewAvailabilityResult:
    def __init__(self, message: str, from_date: date, to_date: date, filtered_by_role: str, data: dict):
        self.message = message
        self.from_date = from_date
        self.to_date = to_date
        self.filtered_by_role = filtered_by_role
        self.data = data
