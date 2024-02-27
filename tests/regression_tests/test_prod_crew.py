from datetime import date
import pytest

from assertpy import assert_that
from dateutil.relativedelta import relativedelta

from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response, AvailableCrew


def test_unbound_crew_availability(regression_test_data):
    from_date, to_date = date.today(), date.today() + relativedelta(months=9)

    response = client.get(f'http://127.0.0.1:8000/crew-availability?from_date={from_date}&to_date={to_date}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .has_Actor(3)\
        .has_Director(2)


def test_unbound_crew_availability_sorted(regression_test_data):
    from_date, to_date = date.today(), date.today() + relativedelta(months=9)

    response = client.get(f'http://127.0.0.1:8000/crew-availability?from_date={from_date}&to_date={to_date}'
                          f'&sort_by=highest_count')

    counts_dict = assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .is_type_of(dict)\
        .val

    assert_that(counts_dict.values(), beautify_response(response))\
        .is_sorted(reverse=True)


def test_unbound_crew_availability_filtered(regression_test_data):
    from_date, to_date = date.today(), date.today() + relativedelta(months=9)

    response = client.get(f'http://127.0.0.1:8000/crew-availability?from_date={from_date}&to_date={to_date}'
                          f'&role=Director')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .has_Director(2)\
        .does_not_contain('Actor')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('filtered_by_role')\
        .is_equal_to('Director')


def test_bound_crew_availability(regression_test_data):
    from_date, to_date = date.today() + relativedelta(years=3, days=1), date.today() + relativedelta(years=5)

    response = client.get(f'http://127.0.0.1:8000/crew-availability?from_date={from_date}&to_date={to_date}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('data')\
        .has_Actor(1)\
        .has_Director(1)


class TestProductionCrew:
    @pytest.mark.parametrize(['title', 'start', 'end', 'crew_req'], [
        (
            'Magnolia',
            str(date.today() + relativedelta(months=3)),
            str(date.today() + relativedelta(months=9)),
            {'Director': 1, 'Actor': 3},
        ),
        (
            'Magnolia 2',
            str(date.today() + relativedelta(years=1, months=3)),
            str(date.today() + relativedelta(years=1, months=9)),
            {'Director': 1, 'Actor': 2},
        )
    ])
    def test_create_production_with_full_and_partial_crew_availability(self, regression_test_data, title, start, end,
                                                                       crew_req):
        # Retrieve crew availability before operation
        prior_crew_availability_resp = client.get(
            f'http://127.0.0.1:8000/crew-availability?from_date={start}&to_date={end}')

        prior_crew_availability = assert_that(prior_crew_availability_resp,
                                              beautify_response(prior_crew_availability_resp))\
            .safe_extract_response_key('data')\
            .val

        # Calculate expected crew availability after operation
        expected_post_crew_availability = AvailableCrew(prior_crew_availability)\
            .subtract_crew(crew_req)

        # Schedule new production
        client.post('http://127.0.0.1:8000/productions/',
                    json={'title': title,
                          'start': start,
                          'end': end,
                          'crew_reqs': crew_req}
                    )

        # Verify new production crew was reserved
        post_crew_availability = client.get(
            f'http://127.0.0.1:8000/crew-availability?from_date={start}&to_date={end}')

        assert_that(post_crew_availability, beautify_response(post_crew_availability))\
            .safe_extract_response_key('data')\
            .is_equal_to(expected_post_crew_availability)

    @pytest.mark.parametrize(['title', 'start', 'end', 'crew_req', 'first_missing_crew_role'], [
        (
            'Magnolia 3',
            str(date.today() + relativedelta(years=2, months=3)),
            str(date.today() + relativedelta(years=2, months=9)),
            {'Director': 1, 'Actor': 1},
            'Director'
        ),
        (
            'Magnolia 4',
            str(date.today() + relativedelta(years=3, months=3)),
            str(date.today() + relativedelta(years=3, months=9)),
            {'Director': 1, 'Actor': 2},
            'Actor'
        )
    ])
    def test_create_production_with_full_and_partial_crew_shortage(self, regression_test_data, title, start, end,
                                                                   crew_req, first_missing_crew_role):

        # Schedule new production
        post_response = client.post('http://127.0.0.1:8000/productions/',
                                    json={'title': title,
                                          'start': start,
                                          'end': end,
                                          'crew_reqs': crew_req}
                                    )

        assert_that(post_response, beautify_response(post_response))\
            .safe_extract_response_key('detail', 500)\
            .is_equal_to(f'Not enough crew members for role: \'{first_missing_crew_role}\'!')

    def test_update_production_with_crew_availability(self, regression_test_data):
        prod_to_update = pytest.regression_prods[0]

        # Extend production by 1 month
        new_prod_dates = {'new_end': str(date.today() + relativedelta(years=3, months=1))}

        put_response = client.put(f'http://127.0.0.1:8000/productions/{prod_to_update.id}', json=new_prod_dates)

        assert_that(put_response, beautify_response(put_response))\
            .safe_extract_response_key('message')\
            .is_equal_to(f'Production dates for show: \'{prod_to_update.id}\', were successfully updated.')

    def test_update_production_with_crew_shortage(self, regression_test_data):
        # Attempt to extend 'Magnolia' production created by prev test - Should fail, not enough crew
        prod_to_update_id = 3

        new_prod_dates = {'new_end': str(date.today() + relativedelta(years=1, months=4))}

        put_response = client.put(f'http://127.0.0.1:8000/productions/{prod_to_update_id}', json=new_prod_dates)

        assert_that(put_response, beautify_response(put_response))\
            .safe_extract_response_key('detail', 500)\
            .is_equal_to('Unable to change production dates, due to other crew obligations during requested timeframe!')

    def test_cancel_production_with_crew(self, regression_test_data):
        prod_to_delete = pytest.regression_prods[1]

        # Retrieve crew availability before operation
        prior_crew_availability_resp = client.get(
            f'http://127.0.0.1:8000/crew-availability?from_date={prod_to_delete.start}&to_date={prod_to_delete.end}')

        prior_crew_availability = assert_that(prior_crew_availability_resp,
                                              beautify_response(prior_crew_availability_resp))\
            .safe_extract_response_key('data')\
            .val

        # Calculate expected crew availability after operation
        expected_post_crew_availability = AvailableCrew(prior_crew_availability)\
            .add_crew({'Actor': 2, 'Director': 1})

        # Verify crew availability before production deletion
        prod_crew_before_del = client.get(
            f'http://127.0.0.1:8000/crew-availability?from_date={prod_to_delete.start}&to_date={prod_to_delete.end}')

        assert_that(prod_crew_before_del)\
            .safe_extract_response_key('data')\
            .is_equal_to({})

        # Delete production
        client.delete(f'http://127.0.0.1:8000/productions/{prod_to_delete.id}')

        # Verify crew availability after production deletion - Crew should be released
        post_crew_availability = client.get(
            f'http://127.0.0.1:8000/crew-availability?from_date={prod_to_delete.start}&to_date={prod_to_delete.end}')

        assert_that(post_crew_availability, beautify_response(post_crew_availability))\
            .safe_extract_response_key('data')\
            .is_equal_to(expected_post_crew_availability)
