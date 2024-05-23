from sqlalchemy import exc
from sqlalchemy import desc # noqa

from service.helpers.query_constructors import construct_crew_order_by_query_substring, validate_crew_member_and_new_fire_date
from models.data.sql_alchemy import Crew, ProdCrew, Production
from models.common import Error


def get_crew_member(db, member_id):
    """
    Retrieves a specific crew member's details from DB.
    """
    try:
        if crew_member := db.query(Crew)\
                .filter(Crew.id == member_id)\
                .first():
            return crew_member
        return Error(f'Crew member with id: \'{member_id}\' not found!', 404)
    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)


def get_all_crew_members(db, name, role, sort_by, limit, offset):
    """
    Retrieves all crew member details from DB.
    """
    if isinstance(order_type := construct_crew_order_by_query_substring(sort_by), Error):
        return order_type

    try:
        query = db.query(Crew)\
            .filter(Crew.full_name == name if name else True)\
            .filter(Crew.role == role if role else True)\
            .order_by(eval(order_type))
        if not (total_recs := query.count()):
            return Error('No crew members found!', 404)
        if total_recs <= offset:
            return Error('Invalid page number, out of bounds!', 400)
        return query.limit(limit).offset(offset).all(), total_recs
    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)


def insert_crew_member(db, role, full_name, hire_date, fire_date):
    """
    Adds a new crew member to DB.
    """
    try:
        new_role = Crew(role=role, full_name=full_name, hire_date=hire_date, fire_date=fire_date)
        db.add(new_role)
        db.commit()
        return new_role.id
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)


def update_crew_member(db, member_id, op_type, fire_date):
    """
    Updates crew member's fire date in DB.
    """
    try:
        # Initiate current transaction
        db.begin()

        # Validate crew member's existence and new fire date
        if isinstance(validation := validate_crew_member_and_new_fire_date(member_id, op_type, fire_date, db), Error):
            raise exc.SQLAlchemyError(validation.message)

        # Updating crew member's fire date
        db.query(Crew)\
            .filter(Crew.id == member_id)\
            .update({'fire_date': fire_date})

        # Moving forward, for transaction to succeed, crew member must not be working during/after fire date
        if any([prod.end > fire_date
                for prod in [db.query(Production)
                             .filter(Production.id == member_prod.prod_id)
                             .first()
                             for member_prod in db.query(ProdCrew)
                             .filter(ProdCrew.crew_id == member_id)
                             .all()]]):

            raise exc.SQLAlchemyError(f'Cannot fire crew member: \'{member_id}\' on: \'{fire_date}\'. '
                                      f'They are engaged in scheduled production!')

        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)
