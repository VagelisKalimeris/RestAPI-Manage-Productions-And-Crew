import pytest
from assertpy import add_extension

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
def smoke_test_data():
    """
    Leaves temporary test db, w/o entries for smoke testing. Removes it after tests completion.
    """
    db = TestingSessionLocal()

    yield

    remove_test_db_data_and_file(db)
