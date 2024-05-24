from sqlalchemy import exc, func, or_
from sqlalchemy import asc, desc # noqa

from service.helpers.query_constructors import construct_crew_availability_order_by_query_substring
from models.data.sql_alchemy import ProdCrew, Production, Crew
from models.common import Error


def get_crew_availability(db, from_date, to_date, role, sort_by):
    """
    Retrieves available crew for given time period.
    """
    if isinstance(order_type := construct_crew_availability_order_by_query_substring(sort_by), Error):
        return order_type

    try:
        # Keep track of not hired or fired crew during timeframe and avoid redundant queries
        unavailable_crew_ids = [row[0] for row in db.query(Crew.id)
                                .filter(or_(Crew.hire_date > from_date, Crew.fire_date <= to_date))
                                .all()]
        # Gather active productions during time frame
        for prod in db.query(Production)\
                .filter(~((Production.end < from_date) | (Production.start > to_date)))\
                .all():
            # Get active crew members
            unavailable_crew_ids.extend([bind.crew_id for bind in db.query(ProdCrew.crew_id)
                                        .filter(ProdCrew.prod_id == prod.id)
                                        .filter(~ProdCrew.crew_id.in_(unavailable_crew_ids))])

        # Return inactive crew member counts for specific period
        return dict(db.query(Crew.role, func.count(Crew.role).label('role_count'))
                    .filter(~Crew.id.in_(unavailable_crew_ids))
                    .filter(Crew.role == role if role else True)
                    .group_by(Crew.role)
                    .order_by(eval(order_type))
                    .all())

    except exc.SQLAlchemyError as e:
        return Error(e.args[0], 500)
