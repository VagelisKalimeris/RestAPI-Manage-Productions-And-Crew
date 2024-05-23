from models.common import Error


def construct_crew_order_by_query_substring(sort_by):
    """
    Constructs the substring required for query results ordering. Verifies input as extra safety.
    """
    match sort_by:
        case 'id':
            return 'Crew.id'
        case 'name':
            return 'Crew.full_name'
        case 'hire_date':
            return 'Crew.hire_date'
        case 'contract_length':
            return 'desc(Crew.fire_date - Crew.hire_date)'
        case None:
            return 'False'
        case _:
            # Input is already validated in service layer. Added for extra safety and possible debug assistance
            return Error(f'Unsupported sort method: \'{sort_by}\'!', 422)


def construct_crew_availability_order_by_query_substring(sort_by):
    """
    Constructs the substring required for query results ordering. Verifies input as extra safety.
    """
    match sort_by:
        case 'highest_count':
            return 'desc("role_count")'
        case 'lowest_count':
            return 'asc("role_count")'
        case None:
            return 'False'
        case _:
            # Input is already validated in service layer. Added for extra safety and possible debug assistance
            return Error(f'Unsupported sort method: \'{sort_by}\'!', 422)


def construct_production_order_by_query_substring(sort_by):
    """
    Constructs the substring required for query results ordering. Verifies input as extra safety.
    """
    match sort_by:
        case 'id':
            return 'Production.id'
        case 'name':
            return 'Production.title'
        case 'start':
            return 'Production.start'
        case 'duration':
            return 'desc(Production.end - Production.start)'
        case None:
            return 'False'
        case _:
            # Input is already validated in service layer. Added for extra safety and possible debug assistance
            return Error(f'Unsupported sort method: \'{sort_by}\'!', 422)


def validate_crew_member_and_new_fire_date(member_id, op_type, fire_date, db):
    """
    Validates given crew member & new fire date against existing one.
    """
    from service.crew import get_crew_member

    if isinstance(crew_member := get_crew_member(db, member_id), Error):
        return crew_member

    if op_type == 'extend' and not fire_date > crew_member.fire_date:
        return Error(f'Can only extend member\'s contract to a date after current fire date: '
                     f'\'{crew_member.fire_date}\'!')

    if op_type == 'shorten' and not fire_date < crew_member.fire_date:
        return Error(f'Can only shorten member\'s contract to a date before current fire date: '
                     f'\'{crew_member.fire_date}\'!')

    return crew_member


def preprocess_production_new_dates(prod_id, new_start, new_end, db):
    """
    Validates given production & new dates against existing ones. Updates them, if necessary.
    """
    from service.productions import get_production

    if isinstance(prod := get_production(db, prod_id), Error):
        return prod

    if new_start == prod.start and new_end == prod.end:
        return Error('At least one of new start or end date must be new!')

    new_start = new_start if new_start else prod.start
    new_end = new_end if new_end else prod.end

    if new_start > new_end:
        return Error('End date cannot be before start date!')

    return new_start, new_end
