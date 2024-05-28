from datetime import date
from dateutil.relativedelta import relativedelta

import pytest
from assertpy import assert_that

from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


@pytest.mark.run(order=2)
def test_get_all_productions(sanity_test_data):
    response = client.get('http://127.0.0.1:8000/productions')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .contains_key('data')\
        .has_message('Details for scheduled productions were successfully retrieved.')\
        .has_pagination({'current_page': 1,
                         'total_pages': 1,
                         'total_records': 1})


@pytest.mark.run(order=2)
def test_retrieve_scheduled_production(sanity_test_data):
    response = client.get(f'http://127.0.0.1:8000/productions/{pytest.sanity_prod.id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .contains_key('data')\
        .has_message('Details for production were successfully retrieved.')\
        .does_not_contain_key('pagination')


@pytest.mark.run(order=2)
def test_retrieve_non_existing_production(sanity_test_data):
    response = client.get(f'http://127.0.0.1:8000/productions/{pytest.non_existing_prod_id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 404)\
        .is_equal_to(f'Production with id: \'{pytest.non_existing_prod_id}\' not found!')


@pytest.mark.run(order=2)
def test_create_production(sanity_test_data):
    response = client.post('http://127.0.0.1:8000/productions',
                           json={
                               'title': 'TEST PROD POST-SANITY',
                               'start': str(date.today()),
                               'end': str(date.today() + relativedelta(years=1)),
                               'crew_reqs': {
                                   'Photographer': 1
                               }
                           })

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None, 201)\
        .contains_key('new_prod_id')\
        .has_message('Production was successfully scheduled.')\
        .does_not_contain_key('data', 'pagination')


@pytest.mark.run(order=2)
def test_update_production(sanity_test_data):
    response = client.patch(f'http://127.0.0.1:8000/productions/{pytest.sanity_prod.id}',
                          json={
                              'new_start': str(pytest.sanity_prod.start + relativedelta(months=1)),
                              'new_end': str(pytest.sanity_prod.end + relativedelta(months=1))
                          })

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .has_message(f"Production dates for show: \'{pytest.sanity_prod.id}\', were successfully updated.")\
        .does_not_contain_key('data', 'pagination')


@pytest.mark.run(order=2)
def test_update_non_existing_production(sanity_test_data):
    response = client.patch(f'http://127.0.0.1:8000/productions/{pytest.non_existing_prod_id}',
                          json={
                              'new_start': str(pytest.sanity_prod.start + relativedelta(months=1)),
                              'new_end': str(pytest.sanity_prod.end + relativedelta(months=1))
                          })

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 500)\
        .is_equal_to(f'Production with id: \'{pytest.non_existing_prod_id}\' not found!')


@pytest.mark.run(order=2)
def test_cancel_production(sanity_test_data):
    response = client.delete(f'http://127.0.0.1:8000/productions/{pytest.sanity_prod.id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .has_message(f'Production with id: \'{pytest.sanity_prod.id}\' was successfully cancelled.')\
        .does_not_contain_key('data', 'pagination')


@pytest.mark.run(order=2)
def test_cancel_non_existing_production(sanity_test_data):
    response = client.delete(f'http://127.0.0.1:8000/productions/{pytest.non_existing_prod_id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 404)\
        .is_equal_to(f'Production with id: \'{pytest.non_existing_prod_id}\' not found!')
