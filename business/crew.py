from service.crew import get_crew_member, get_all_crew_members, insert_crew_member, update_crew_member


def retrieve_all_crew_members(db, name, role, sort_by, limit, offset):
    """
    Retrieves details for specific crew member.
    """
    return get_all_crew_members(db, name, role, sort_by, limit, offset)


def retrieve_specific_crew_member(db, member_id):
    """
    Retrieves details for specific crew member.
    """
    return get_crew_member(db, member_id)


def hire_crew_member(db, crew_member_details):
    """
    Hires a new crew member.
    """
    return insert_crew_member(db, crew_member_details.role, crew_member_details.full_name,
                              crew_member_details.hire_date, crew_member_details.fire_date)


def update_crew_member_fire_date(db, member_id, op_type, new_fire_date):
    """
    Fires an existing crew member.
    """
    return update_crew_member(db, member_id, op_type, new_fire_date)
