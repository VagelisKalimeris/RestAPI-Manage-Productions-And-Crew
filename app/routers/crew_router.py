from datetime import date
from math import ceil
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session

from app.config import DEFAULT_PAGE_SIZE
from app.routers.router_dependencies import get_db
from app.models.shared.shared_models import PrettyJSONResponse, Error
from app.models.route.pagination_models import PaginationResult
from app.models.route.crew_models import CrewMember, SortCrewBy, AllCrewMembersResult, CrewMemberResult, HireResult, \
    FireResult, Member
from app.services.crew_service import get_all_crew_members, get_crew_member, hire_crew_member, \
    update_crew_member_fire_date


router = APIRouter()


@router.get('/crew', status_code=200, response_class=PrettyJSONResponse)
def detail_all_crew_members(name: str = None, role: str = None, sort_by: SortCrewBy = None,
                            page_size: Annotated[int, Query(ge=1)] = DEFAULT_PAGE_SIZE,
                            page_num: Annotated[int, Query(ge=1)] = 1,
                            db: Session = Depends(get_db)) -> AllCrewMembersResult:
    """
    Returns all existing crew member details.
    """
    # Check for errors
    if isinstance(crew := get_all_crew_members(db, name, role, sort_by, page_size, (page_num - 1) * page_size), Error):
        raise HTTPException(status_code=crew.status, detail=crew.message)

    return AllCrewMembersResult(
        message='Crew members successfully retrieved.',
        data=[
            Member(
                role=member.role,
                full_name=member.full_name,
                hire_date=member.hire_date,
                fire_date=member.fire_date,
                id=member.id
            )
            for member in crew[0]
        ],
        pagination=PaginationResult(
            total_records=crew[1],
            current_page=page_num,
            total_pages=ceil(crew[1] / page_size)
        )
    )


@router.get('/crew/{member_id}', status_code=200, response_class=PrettyJSONResponse)
def detail_specific_crew_member(member_id: int, db: Session = Depends(get_db)) -> CrewMemberResult:
    """
    Returns specific crew member's details.
    """
    # Check for errors
    if isinstance(crew_member := get_crew_member(db, member_id), Error):
        raise HTTPException(status_code=crew_member.status, detail=crew_member.message)

    return CrewMemberResult(
        message='Crew member info successfully retrieved.',
        data=Member(
            role=crew_member.role,
            full_name=crew_member.full_name,
            hire_date=crew_member.hire_date,
            fire_date=crew_member.fire_date,
            id=crew_member.id
        )
    )


@router.post('/crew/', status_code=200, response_class=PrettyJSONResponse)
def hire_new_crew_member(crew_member_details: CrewMember, db: Session = Depends(get_db)) -> HireResult:
    """
    Hires new crew member on given start date. Members with the same name can exist, since they will be assigned
    different ids. Fire date is optional, if not given they are considered permanent.
    """
    # Check for errors
    if isinstance(crew_member_hire := hire_crew_member(db, crew_member_details.role, crew_member_details.full_name,
                                                       crew_member_details.hire_date, crew_member_details.fire_date),
                  Error):
        raise HTTPException(status_code=crew_member_hire.status, detail=crew_member_hire.message)

    return HireResult(
        message='Crew member hired successfully.',
        new_member_id=crew_member_hire
    )


@router.patch('/crew/{member_id}/', status_code=200, response_class=PrettyJSONResponse)
def update_fire_date_for_existing_crew_member(member_id: int, op_type: Literal['extend', 'shorten'],
                                              new_date: Annotated[date, Body()], db: Session = Depends(get_db)) \
        -> FireResult:
    """
    Fires existing crew member on given end date.
    """
    # Check for errors
    if isinstance(crew_member := update_crew_member_fire_date(db, member_id, op_type, new_date), Error):
        raise HTTPException(status_code=crew_member.status, detail=crew_member.message)

    return FireResult(
        message='Crew member fire date updated successfully.'
    )
