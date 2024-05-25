from sqlalchemy import exc, and_
from sqlalchemy import desc # noqa

from app.services.helpers.query_constructors import construct_production_order_by_query_substring, \
    preprocess_production_new_dates
from app.models.data.sql_alchemy_models import Production, ProdCrew, Crew
from app.models.shared.shared_models import Error
from app.services.helpers.date_validators import date_ranges_overlap


def get_all_scheduled_productions(db, min_date, max_date, title, sort_by, limit, offset):
    """
    Queries db for all productions.
    """
    if isinstance(order_type := construct_production_order_by_query_substring(sort_by), Error):
        return order_type

    try:
        query = db.query(Production)\
            .filter(Production.start >= min_date)\
            .filter(Production.end <= max_date)\
            .filter(Production.title == title if title else True)\
            .order_by(eval(order_type))
        if not (total_recs := query.count()):
            return Error('No productions found!', 404)
        if total_recs <= offset:
            return Error('Invalid page number, out of bounds!', 400)
        return query.limit(limit).offset(offset).all(), total_recs
    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)


def get_scheduled_production(db, prod_id):
    """
    Queries db for specific production.
    """
    try:
        if prod := db.query(Production)\
                .filter(Production.id == prod_id)\
                .first():
            return prod
        return Error(f'Production with id: \'{prod_id}\' not found!', 404)
    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)


def schedule_production(db, title, start, end, crew_reqs):
    """
    Adds new production to db.
    """
    try:
        # Initiate current transaction by adding the production
        new_prod = Production(title=title, start=start, end=end)
        db.add(new_prod)
        db.flush()

        # Moving forward, for transaction to succeed, all roles demands need to be fulfilled
        for role, required_role_count in crew_reqs.items():

            # Bind any active & available crew members with this role
            members_bound, checked_prod_ids = 0, []
            for member in db.query(Crew)\
                    .filter(Crew.role == role)\
                    .filter(and_(Crew.hire_date <= start, Crew.fire_date > end))\
                    .all():
                if members_bound == required_role_count:
                    # We filled current role demands
                    break

                # None of existing productions using current member can overlap with new production timeframe
                overlap = False
                for bind in db.query(ProdCrew)\
                        .filter(ProdCrew.crew_id == member.id)\
                        .filter(~ProdCrew.prod_id.in_(checked_prod_ids))\
                        .all():
                    prod = db.query(Production)\
                        .filter(Production.id == bind.prod_id)\
                        .first()
                    if date_ranges_overlap(prod.start, prod.end, start, end):
                        overlap = True
                        break
                    else:
                        checked_prod_ids.append(prod.id)

                if not overlap:
                    # Current crew member is available, bind to new production
                    new_prod_crew = ProdCrew(prod_id=new_prod.id, crew_id=member.id)
                    db.add(new_prod_crew)
                    members_bound += 1

            # Stop if role availability does not meet demand
            if members_bound < required_role_count:
                raise exc.SQLAlchemyError(f'Not enough crew members for role: \'{role}\'!')

        db.commit()
        return new_prod.id
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)


def update_production_dates(db, prod_id, new_start, new_end):
    """
    Updates existing production dates in db.
    """
    try:
        # Initiate current transaction
        db.begin()

        # Validate production's existence and new dates against existing ones
        if isinstance(validation := preprocess_production_new_dates(prod_id, new_start, new_end, db), Error):
            raise exc.SQLAlchemyError(validation.message)

        new_start, new_end = validation

        # Updating production
        db.query(Production)\
            .filter(Production.id == prod_id)\
            .update({'start': new_start, 'end': new_end})

        # Moving forward, for transaction to succeed, all production crew must be available during new timeframe
        checked_prod_ids = []
        for crew_id in [row[0] for row in db.query(ProdCrew.crew_id).filter(ProdCrew.prod_id == prod_id).all()]:
            # First check member's contract is active during new period
            crew_member = db.query(Crew.hire_date, Crew.fire_date)\
                .filter(Crew.id == crew_id)\
                .first()
            if not (crew_member.hire_date <= new_start and crew_member.fire_date > new_end):
                raise exc.SQLAlchemyError('Unable to change production dates, due to crew member fire date conflict!')

            # Gather other productions using current crew member
            crew_member_prod_ids = [row[0] for row in db.query(ProdCrew.prod_id)
                                    .filter(ProdCrew.crew_id == crew_id)
                                    .filter(ProdCrew.prod_id != prod_id)
                                    .filter(~ProdCrew.prod_id.in_(checked_prod_ids))
                                    .all()]

            for member_prod_id in crew_member_prod_ids:
                member_prod = db.query(Production)\
                    .filter(Production.id == member_prod_id)\
                    .first()
                if date_ranges_overlap(new_start, new_end, member_prod.start, member_prod.end):
                    # Cannot schedule - Abort
                    raise exc.SQLAlchemyError('Unable to change production dates, due to other crew obligations '
                                              'during requested timeframe!')
                checked_prod_ids.append(member_prod_id)

        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)


def delete_existing_production(db, prod_id):
    """
    Drops existing production from db.
    """
    try:
        # Check if prod exists before proceeding
        if not db.query(Production)\
                .filter(Production.id == prod_id)\
                .first():
            return Error(f'Production with id: \'{prod_id}\' not found!', 404)

        # Initiate current transaction by deleting the production
        db.query(Production)\
            .filter(Production.id == prod_id)\
            .delete()

        # Moving forward, for transaction to succeed, all production crew must be unbound
        db.query(ProdCrew)\
            .filter(ProdCrew.prod_id == prod_id)\
            .delete()

        db.commit()
    except exc.SQLAlchemyError as e:
        db.rollback()
        return Error(e.args[0], 500)
