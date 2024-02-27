from enum import Enum


class SortCrewAvailabilityBy(str, Enum):
    """
    Purposed for GET request params validation.
    """
    highest_count = 'highest_count'
    lowest_count = 'lowest_count'
