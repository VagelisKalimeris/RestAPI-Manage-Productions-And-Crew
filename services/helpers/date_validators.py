from datetime import date

from models.shared.shared_models import Error


def validate_start_end_dates(start_date, end_date):
    """
    Validates start date is not before end date, and start date is not past.
    """
    if start_date > end_date:
        return Error('End date cannot be before start date!', 422)
    if start_date < date.today():
        return Error('Start date cannot be past!', 422)


def date_ranges_overlap(start_date_a, end_date_a, start_date_b, end_date_b):
    """
    Checks if two date ranges overlap with each other.
    """
    return not (start_date_a > end_date_b or end_date_a < start_date_b)
