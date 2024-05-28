import pytest

from .regression_test_data.regression_test_db_entries import regression_crew, regression_prods, regression_bindings
from tests.testing_dependencies.create_test_db_and_test_client import TestingSessionLocal
from tests.testing_dependencies.delete_test_data_and_db import remove_test_db_data_and_file


@pytest.fixture(scope='module')
def regression_test_data():
    """
    Populates temporary test db with data required for regression testing. Removes test data and DB after tests
    completion.
    """
    db = TestingSessionLocal()

    # Populate DB with test data
    db.bulk_save_objects(regression_crew + regression_prods + regression_bindings)
    db.commit()

    # Cache test data for easy discovery by tests
    pytest.regression_crew = regression_crew
    pytest.regression_prods = regression_prods

    yield

    remove_test_db_data_and_file(db)
