import pytest

from tests.testing_dependencies.create_test_db_and_test_client import TestingSessionLocal
from tests.testing_dependencies.delete_test_data_and_db import remove_test_db_data_and_file


@pytest.fixture(scope='module')
def smoke_test_data():
    """
    Leaves temporary test db, w/o entries for smoke testing. Removes it after tests completion.
    """
    db = TestingSessionLocal()

    yield

    remove_test_db_data_and_file(db)
