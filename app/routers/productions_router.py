from datetime import date
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.config import DEFAULT_PAGE_SIZE
from app.services.productions_service import get_all_scheduled_productions, schedule_production, \
    get_scheduled_production, update_production_dates, delete_existing_production
from app.routers.router_dependencies import get_db
from app.models.shared.shared_models import PrettyJSONResponse, Error
from app.models.route.pagination_models import PaginationResult
from app.models.route.productions_models import ProductionDetails, SortProductionsBy, NewProdDates, \
    AllProductionsResult, ProductionResult, NewProductionResult, UpdateProductionResult, CancelProductionResult

router = APIRouter()


@router.get('/productions', status_code=200, response_class=PrettyJSONResponse)
def retrieve_all_scheduled_productions(min_date: date | None = date.min, max_date: date | None = date.max,
                                       title: str = None, sort_by: SortProductionsBy = None,
                                       page_size: Annotated[int, Query(ge=1)] = DEFAULT_PAGE_SIZE,
                                       page_num: Annotated[int, Query(ge=1)] = 1, db: Session = Depends(get_db)):
    """
    Returns all scheduled productions details. Optional start/end dates filter results to given time range.
    """
    # Check for errors
    if isinstance(prods := get_all_scheduled_productions(db, min_date, max_date, title, sort_by, page_size,
                                                         (page_num - 1) * page_size), Error):
        raise HTTPException(status_code=prods.status, detail=prods.message)

    return AllProductionsResult('Details for scheduled productions were successfully retrieved.', prods[0],
                                PaginationResult(prods[1], page_num, ceil(prods[1] / page_size))).__dict__


@router.get('/productions/{prod_id}', status_code=200, response_class=PrettyJSONResponse)
def retrieve_scheduled_production(prod_id: int, db: Session = Depends(get_db)):
    """
    Returns specific scheduled production details.
    """
    if isinstance(prod := get_scheduled_production(db, prod_id), Error):
        # Check for errors
        raise HTTPException(status_code=prod.status, detail=prod.message)

    return ProductionResult('Details for production were successfully retrieved.', prod).__dict__


@router.post('/productions', status_code=201, response_class=PrettyJSONResponse)
def create_production(prod_details: ProductionDetails, db: Session = Depends(get_db)):
    """
    Registers given production.
    """
    # Check for errors
    if isinstance(new_prod := schedule_production(db, prod_details.title, prod_details.start, prod_details.end,
                                                  prod_details.crew_reqs), Error):
        raise HTTPException(status_code=new_prod.status, detail=new_prod.message)

    return NewProductionResult('Production was successfully scheduled.', new_prod).__dict__


@router.patch('/productions/{prod_id}', status_code=200, response_class=PrettyJSONResponse)
def update_production(prod_id: int, new_dates: NewProdDates, db: Session = Depends(get_db)):
    """
    Updates given production's dates, as long as no crew scheduling conflicts arise.
    """
    # Check for errors
    if isinstance(updated_prod := update_production_dates(db, prod_id, new_dates.new_start,
                                                          new_dates.new_end), Error):
        raise HTTPException(status_code=updated_prod.status, detail=updated_prod.message)

    return UpdateProductionResult(f'Production dates for show: \'{prod_id}\', were successfully updated.').__dict__


@router.delete('/productions/{prod_id}', status_code=200, response_class=PrettyJSONResponse)
def cancel_production(prod_id: str, db: Session = Depends(get_db)):
    """
    Deletes given production.
    """
    # Check for errors
    if isinstance(deleted_prod := delete_existing_production(db, prod_id), Error):
        raise HTTPException(status_code=deleted_prod.status, detail=deleted_prod.message)

    return CancelProductionResult(f'Production with id: \'{prod_id}\' was successfully cancelled.').__dict__
