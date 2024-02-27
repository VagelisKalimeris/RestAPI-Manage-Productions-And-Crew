import pytest
from assertpy import assert_that

from tests.testing_dependencies.create_test_db_and_test_client import client
from tests.testing_dependencies.util import beautify_response


@pytest.mark.run(order=1)
def test_detail_all_crew_members_wo_db_entries(smoke_test_data):
    response = client.get('http://127.0.0.1:8000/crew')

    assert_that(response, beautify_response(response))\
        .safe_extract_response_key('detail', 404)\
        .is_equal_to('No crew members found!')
