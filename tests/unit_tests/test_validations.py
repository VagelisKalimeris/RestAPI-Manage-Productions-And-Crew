from types import NoneType
from datetime import date

import pytest
from assertpy import assert_that

from app.models.shared.shared_models import Error
from app.services.helpers.date_validators import validate_start_end_dates, date_ranges_overlap


@pytest.mark.run(order=0)
@pytest.mark.parametrize(['start_date', 'end_date', 'expected_result_type'], [
    # Passing ranges
    (date(2030, 1, 1), date(2031, 1, 1), NoneType),
    (date(2035, 1, 1), date(2035, 1, 2), NoneType),
    # Error start date after end date
    (date(2001, 2, 1), date(2003, 1, 1), Error),
    # Error past start date
    (date(2000, 1, 1), date(2030, 1, 1), Error),
])
def test_validate_start_end_dates(start_date, end_date, expected_result_type):
    # Verify expected behaviour
    assert_that(validate_start_end_dates(start_date, end_date))\
        .is_instance_of(expected_result_type)


@pytest.mark.run(order=0)
@pytest.mark.parametrize(['start_date_a', 'end_date_a', 'start_date_b', 'end_date_b', 'expected_result'], [
    # Non overlapping ranges
    (date(2000, 1, 1), date(2001, 1, 1), date(2002, 1, 1), date(2003, 1, 1), False),
    (date(2002, 1, 1), date(2003, 1, 1), date(2000, 1, 1), date(2000, 1, 1), False),
    # Overlapping ranges
    (date(2002, 1, 1), date(2003, 1, 1), date(2001, 1, 1), date(2004, 1, 1), True),
    (date(2000, 1, 1), date(2003, 1, 1), date(2001, 1, 1), date(2002, 1, 1), True),
    # Edge cases
    (date(2000, 1, 1), date(2003, 1, 1), date(2003, 1, 1), date(2005, 1, 1), True),
    (date(2000, 1, 1), date(2003, 1, 1), date(2003, 1, 2), date(2005, 1, 1), False)
])
def test_date_ranges_overlap(start_date_a, end_date_a, start_date_b, end_date_b, expected_result):
    # Verify expected behaviour
    assert_that(date_ranges_overlap(start_date_a, end_date_a, start_date_b, end_date_b))\
        .is_equal_to(expected_result)
