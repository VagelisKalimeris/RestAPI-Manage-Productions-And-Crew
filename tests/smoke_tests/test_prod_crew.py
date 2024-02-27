from datetime import date

import pytest
from assertpy import assert_that

from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


@pytest.mark.run(order=1)
def test_retrieve_crew_availability_wo_db_entries(smoke_test_data):
    from_date, to_date = date.today(), date.max

    response = client.get(f'http://127.0.0.1:8000/crew-availability?from_date={from_date}&to_date={to_date}')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key(None)\
        .has_message('Crew availability was successfully retrieved.')\
        .has_from_date(str(from_date))\
        .has_to_date(str(to_date))\
        .has_filtered_by_role(None)\
        .has_data({})
