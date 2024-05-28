from datetime import date
from dateutil.relativedelta import relativedelta

import pytest
from assertpy import assert_that

from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


@pytest.mark.run(order=2)
def test_detail_all_crew_members(sanity_test_data):
    response = client.get('http://127.0.0.1:8000/crew')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .contains_key('data')\
        .has_message('Crew members successfully retrieved.')\
        .has_pagination({'current_page': 1,
                         'total_pages': 1,
                         'total_records': 1})


@pytest.mark.run(order=2)
def test_detail_specific_crew_member(sanity_test_data):
    response = client.get(f'http://127.0.0.1:8000/crew/{pytest.sanity_member.id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .contains_key('data')\
        .does_not_contain_key('pagination')\
        .has_message('Crew member info successfully retrieved.')


@pytest.mark.run(order=2)
def test_detail_non_existing_crew_member(sanity_test_data):
    response = client.get(f'http://127.0.0.1:8000/crew/{pytest.non_existing_member_id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 404)\
        .is_equal_to(f'Crew member with id: \'{pytest.non_existing_member_id}\' not found!')


@pytest.mark.run(order=2)
def test_hire_new_crew_member(sanity_test_data):
    response = client.post('http://127.0.0.1:8000/crew/',
                           json={
                               'fire_date': str(date.max),
                               'full_name': 'TEST MEMBER POST-SANITY',
                               'hire_date': str(date.today()),
                               'role': 'Director'
                           })

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .contains_key('new_member_id')\
        .does_not_contain_key('data', 'pagination')\
        .has_message('Crew member hired successfully.')


@pytest.mark.run(order=2)
def test_update_fire_date_for_existing_crew_member(sanity_test_data):
    response = client.patch(f'http://localhost:8000/crew/{pytest.sanity_member.id}/?op_type=extend',
                          json=str(date.today() + relativedelta(years=3)))

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .has_message('Crew member fire date updated successfully.')\
        .does_not_contain_key('data', 'pagination', 'new_member_id')


@pytest.mark.run(order=2)
def test_update_fire_date_for_non_existing_crew_member(sanity_test_data):
    response = client.patch(f'http://localhost:8000/crew/{pytest.non_existing_member_id}/?op_type=extend',
                          json=str(date.today() + relativedelta(years=3)))

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 500)\
        .is_equal_to(f'Crew member with id: \'{pytest.non_existing_member_id}\' not found!')
