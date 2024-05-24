from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from services.helpers.date_validators import validate_start_end_dates
from services.prod_crew_service import get_crew_availability
from routers.router_dependencies import get_db
from models.shared.shared_models import PrettyJSONResponse, Error
from models.route.prod_crew_models import SortCrewAvailabilityBy

router = APIRouter()


@router.get('/crew-availability', status_code=200, response_class=PrettyJSONResponse)
def retrieve_crew_availability(from_date: date, to_date: date, role: str = None,
                               sort_by: SortCrewAvailabilityBy = None,
                               db: Session = Depends(get_db)):
    """
    Returns available crew role counts for specific date range.
    """
    # Check dates validity
    if isinstance(dates_analysis := validate_start_end_dates(from_date, to_date), Error):
        raise HTTPException(status_code=dates_analysis.status, detail=dates_analysis.message)

    if isinstance(crew_counts := get_crew_availability(db, from_date, to_date, role, sort_by), Error):
        raise HTTPException(status_code=crew_counts.status, detail=crew_counts.message)

    return {
        'message': 'Crew availability was successfully retrieved.',
        'from_date': from_date,
        'to_date': to_date,
        'filtered_by_role': role,
        'data': crew_counts
    }
