import pytest
from assertpy import add_extension

from .sanity_test_data.sanity_test_db_entries import sanity_member, sanity_prod
from tests.testing_dependencies.create_test_db_and_test_client import TestingSessionLocal
from tests.testing_dependencies.delete_test_data_and_db import remove_test_db_data_and_file
from tests.testing_dependencies.assertpy_extensions import safe_extract_response_key


@pytest.fixture(scope='module', autouse=True)
def custom_extensions():
    """
    Makes custom extensions available to all module tests.
    """
    add_extension(safe_extract_response_key)


@pytest.fixture(scope='module')
def sanity_test_data():
    """
    Populates temporary test db with data required for sanity testing. Removes test data and DB after tests
    completion.
    """
    db = TestingSessionLocal()

    # Populate DB with test data
    db.bulk_save_objects([sanity_member, sanity_prod])
    db.commit()

    # Cache test data for easy discovery by tests
    pytest.sanity_member, pytest.sanity_prod = sanity_member, sanity_prod
    pytest.non_existing_member_id = pytest.non_existing_prod_id = 9999

    yield

    remove_test_db_data_and_file(db)
