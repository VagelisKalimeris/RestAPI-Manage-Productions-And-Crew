from data_access.productions import add_production, get_all_productions, get_production, update_production_dates, \
    drop_production


def get_all_scheduled_productions(db, min_date, max_date, title, sort_by, limit, offset):
    """
    Retrieves details for all productions for given date range.
    """
    return get_all_productions(db, min_date, max_date, title, sort_by, limit, offset)


def get_scheduled_production(db, prod_id):
    """
    Retrieves details for specific production.
    """
    return get_production(db, prod_id)


def schedule_production(db, prod_details):
    """
    Schedules new production.
    """
    return add_production(db, prod_details)


def update_existing_production(db, prod_id, new_start, new_end):
    """
    Updates existing production.
    """
    return update_production_dates(db, prod_id, new_start, new_end)


def delete_existing_production(db, prod_id):
    """
    Deletes existing production.
    """
    return drop_production(db, prod_id)
