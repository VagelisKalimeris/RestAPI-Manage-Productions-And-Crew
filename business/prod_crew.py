from data_access.prod_crew import get_crew_availability


def retrieve_available_crew(db, from_date, to_date, role, sort_by):
    """
    Retrieves details for all roles.
    """
    return get_crew_availability(db, from_date, to_date, role, sort_by)
