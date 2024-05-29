from datetime import date
from math import ceil

import pytest
from assertpy import assert_that
from dateutil.relativedelta import relativedelta

from app.config import DEFAULT_PAGE_SIZE
from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


def test_detail_all_crew_members(regression_test_data):
    existing_crew_member = pytest.regression_crew[2]
    expected_total_records = len(pytest.regression_crew)

    response = client.get('http://127.0.0.1:8000/crew')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_length(expected_total_records)\
        .contains({'fire_date': str(existing_crew_member.fire_date),
                   'full_name': existing_crew_member.full_name,
                   'hire_date': str(existing_crew_member.hire_date),
                   'id': existing_crew_member.id,
                   'role': existing_crew_member.role})

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('pagination')\
        .is_equal_to({'current_page': 1,
                      'total_pages': ceil(expected_total_records / DEFAULT_PAGE_SIZE),
                      'total_records': expected_total_records})


def test_filter_all_crew_members_by_role(regression_test_data):
    response = client.get('http://127.0.0.1:8000/crew?role=Director')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .extracting('role')\
        .contains('Director')\
        .does_not_contain('Actor')


@pytest.mark.parametrize('sort_by', ['id', 'hire_date'])
def test_sorting_all_crew_members(regression_test_data, sort_by):
    response = client.get(f'http://127.0.0.1:8000/crew?sort_by={sort_by}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .extracting(sort_by)\
        .is_sorted()


def test_detail_specific_crew_member(regression_test_data):
    existing_crew_member = pytest.regression_crew[3]

    response = client.get(f'http://127.0.0.1:8000/crew/{pytest.regression_crew[3].id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_equal_to({'fire_date': str(existing_crew_member.fire_date),
                      'full_name': existing_crew_member.full_name,
                      'hire_date': str(existing_crew_member.hire_date),
                      'id': existing_crew_member.id,
                      'role': existing_crew_member.role})


class TestHireFireNewCrewMember:
    def test_hire_new_crew_member(self, regression_test_data):
        new_member = {'full_name': 'TEST MEMBER POST-REGRESSION',
                      'hire_date': str(date.today()),
                      'fire_date': str(date.max),
                      'role': 'Director'}

        # Hire new employee
        post_response = client.post('http://127.0.0.1:8000/crew/', json=new_member)

        new_member_id = assert_that(post_response, beautify_response(post_response))\
            .safe_extract_response_key('new_member_id')\
            .val

        # Verify new employee is indeed hired
        get_response = client.get(f'http://127.0.0.1:8000/crew/{new_member_id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .is_equal_to(new_member, ignore='id')

        # Save new member id for next test
        pytest.regression_new_member_id = new_member_id

    def test_fire_new_crew_member(self, regression_test_data):
        # Fire new employee 1 month from now
        client.patch(f'http://localhost:8000/crew/{pytest.regression_new_member_id}/?op_type=shorten',
                     json=str(date.today() + relativedelta(months=1)))

        # Verify employee is fired
        get_response = client.get(f'http://127.0.0.1:8000/crew/{pytest.regression_new_member_id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .has_fire_date(str(date.today() + relativedelta(months=1)))


class TestFireExistingCrewMember:
    def test_fire_existing_crew_member(self, regression_test_data):
        member_to_fire = pytest.regression_crew[2]

        # Fire an employee right after their last binding has ended
        client.patch(f'http://localhost:8000/crew/{member_to_fire.id}/?op_type=shorten',
                     json=str(date.today() + relativedelta(years=4, days=1)))

        # Verify employee is indeed fired
        get_response = client.get(f'http://127.0.0.1:8000/crew/{member_to_fire.id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .has_fire_date(str(date.today() + relativedelta(years=4, days=1)))

    @pytest.mark.parametrize('new_fire_date', [
        str(date.today() + relativedelta(years=3)),
        str(date.today() + relativedelta(years=1))
    ])
    def test_fire_existing_crew_member_during_production_engagement(self, regression_test_data, new_fire_date):
        member_to_fire = pytest.regression_crew[3]

        # Attempt to fire an employee before their last binding has ended
        patch_response = client.patch(f'http://localhost:8000/crew/{member_to_fire.id}/?op_type=shorten',
                                      json=new_fire_date)

        # Verify employee is CANNOT be fired
        assert_that(patch_response, beautify_response(patch_response))\
            .safe_extract_response_key('detail', 500)\
            .contains('Cannot fire crew member:')\
            .contains('They are engaged in scheduled production!')

        # Verify employee status is unaffected
        get_response = client.get(f'http://127.0.0.1:8000/crew/{member_to_fire.id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .has_fire_date(str(member_to_fire.fire_date))
