import os

from persistence.sql_alch_models import Crew, Production, ProdCrew


def drop_all_test_db_data(db):
    """
    Deletes all db table entries.
    """
    db.query(Crew).delete()
    db.query(Production).delete()
    db.query(ProdCrew).delete()

    db.commit()
    db.close()


def remove_test_db_file():
    """
    Deletes the test database.
    """
    if os.path.exists('production.db'):
        os.remove('production.db')


def remove_test_db_data_and_file(db):
    """
    Delete all db entries & file after the tests end.
    """
    drop_all_test_db_data(db)
    remove_test_db_file()
