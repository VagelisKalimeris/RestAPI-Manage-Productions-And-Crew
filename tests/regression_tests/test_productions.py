from datetime import date
from math import ceil

import pytest
from assertpy import assert_that
from dateutil.relativedelta import relativedelta

from app.config import DEFAULT_PAGE_SIZE
from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


def test_retrieve_all_scheduled_productions(regression_test_data):
    existing_prod = pytest.regression_prods[0]

    response = client.get('http://127.0.0.1:8000/productions')

    expected_total_records = len(pytest.regression_prods)

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_length(expected_total_records)\
        .contains({'title': existing_prod.title,
                   'start': str(existing_prod.start),
                   'end': str(existing_prod.end),
                   'id': existing_prod.id})

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('pagination')\
        .is_equal_to({'current_page': 1,
                      'total_pages': ceil(expected_total_records / DEFAULT_PAGE_SIZE),
                      'total_records': expected_total_records})


def test_filter_all_scheduled_productions_by_date(regression_test_data):
    min_date, max_date = date.today() + relativedelta(years=1), date.today() + relativedelta(years=3)
    prod_during_dates, prod_out_of_dates = pytest.regression_prods[0], pytest.regression_prods[1]

    response = client.get(f'http://127.0.0.1:8000/productions?min_date={min_date}&max_date={max_date}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .extracting('title')\
        .contains(prod_during_dates.title)\
        .does_not_contain(prod_out_of_dates.title)


def test_filter_all_scheduled_productions_by_title(regression_test_data):
    existing_prod = pytest.regression_prods[1]

    response = client.get(f'http://127.0.0.1:8000/productions?title={existing_prod.title}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_equal_to([{'title': existing_prod.title,
                       'start': str(existing_prod.start),
                       'end': str(existing_prod.end),
                       'id': existing_prod.id}])


@pytest.mark.parametrize('sort_by', ['id', 'start'])
def test_sorting_all_scheduled_productions(regression_test_data, sort_by):
    response = client.get(f'http://127.0.0.1:8000/productions?sort_by={sort_by}')

    assert_that(response, beautify_response(response)) \
        .safe_extract_response_key('data') \
        .extracting(sort_by) \
        .is_sorted()


def test_retrieve_scheduled_production(regression_test_data):
    prod_to_retrieve = pytest.regression_prods[0]

    # Retrieve existing production
    response = client.get(f'http://127.0.0.1:8000/productions/{prod_to_retrieve.id}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_equal_to({'title': prod_to_retrieve.title,
                      'start': str(prod_to_retrieve.start),
                      'end': str(prod_to_retrieve.end),
                      'id': prod_to_retrieve.id})


class TestNewProductionWithoutCrew:
    def test_create_production_no_crew(self, regression_test_data):
        new_prod = {'title': 'Iron Man 2',
                    'start': str(date.today() + relativedelta(years=2)),
                    'end': str(date.today() + relativedelta(years=3)),
                    'crew_reqs': {}}

        # Schedule new production
        post_response = client.post('http://127.0.0.1:8000/productions/', json=new_prod)

        new_prod_id = assert_that(post_response, beautify_response(post_response))\
            .safe_extract_response_key('new_prod_id', 201)\
            .val

        # Verify new production
        get_response = client.get(f'http://127.0.0.1:8000/productions/{new_prod_id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .is_equal_to(new_prod, ignore=['crew_reqs', 'id'])

        # Save new prod id for next test
        pytest.regression_new_prod_id = new_prod_id

    def test_update_production_no_crew(self, regression_test_data):
        # Retrieve id from production created by prev test
        prod_to_update_id = pytest.regression_new_prod_id

        # Delay production start/end by 1 month
        new_prod_dates = {'new_start': str(date.today() + relativedelta(years=1, months=1)),
                          'new_end': str(date.today() + relativedelta(years=2, months=1))}

        client.patch(f'http://127.0.0.1:8000/productions/{prod_to_update_id}', json=new_prod_dates)

        # Verify dates are changed
        get_response = client.get(f'http://127.0.0.1:8000/productions/{prod_to_update_id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('data')\
            .has_start(new_prod_dates['new_start'])\
            .has_end(new_prod_dates['new_end'])

    def test_cancel_production_no_crew(self, regression_test_data):
        # Retrieve id from production created by prev test
        prod_to_delete_id = pytest.regression_new_prod_id

        # Delete existing production
        client.delete(f'http://127.0.0.1:8000/productions/{prod_to_delete_id}')

        # Verify production no more exists
        get_response = client.get(f'http://127.0.0.1:8000/productions/{prod_to_delete_id}')

        assert_that(get_response, beautify_response(get_response))\
            .safe_extract_response_key('detail', 404)\
            .is_equal_to(f'Production with id: \'{prod_to_delete_id}\' not found!')
