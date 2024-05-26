from enum import Enum
from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.models.shared.shared_models import PaginationResult


class ProductionDetails(BaseModel):
    """
    Purposed for POST request body validation.
    """
    title: str
    start: date
    end: date
    crew_reqs: dict[str, int] = Field(json_schema_extra={'example': '{"role_1": 3, "role_2": 1, "role_3": 4}'})

    @model_validator(mode='after')
    def dates_are_valid(self):
        if self.start < date.today():
            raise ValueError('Cannot schedule production starting on past date!')
        if self.end <= self.start:
            raise ValueError('Production cannot end, before start date!')
        return self


class NewProdDates(BaseModel):
    """
    Purposed for POST request body validation.
    """
    new_start: date = None
    new_end: date = None

    @model_validator(mode='after')
    def dates_are_valid(self):
        if not (self.new_end or self.new_start):
            raise ValueError('No date given to update!')
        if self.new_start and self.new_start < date.today():
            raise ValueError('Νew production start date cannot be past!')
        if self.new_end and self.new_start and self.new_end <= self.new_start:
            raise ValueError('Νew production end date, cannot be before start date!')
        return self


class SortProductionsBy(str, Enum):
    """
    Purposed for GET request params validation.
    """
    id = 'id'
    name = 'name'
    start = 'start'
    duration = 'duration'


class AllProductionsResult:
    """
    GET all productions response template.
    """
    def __init__(self, message: str, data: dict, pagination: PaginationResult):
        self.message = message
        self.data = data
        self.pagination = pagination


class ProductionResult:
    """
    GET production response template.
    """
    def __init__(self, message: str, data: dict):
        self.message = message
        self.data = data


class NewProductionResult:
    """
    Schedule production response template.
    """
    def __init__(self, message: str, new_prod_id: int):
        self.message = message
        self.new_prod_id = new_prod_id


class UpdateProductionResult:
    """
    Update production response template.
    """
    def __init__(self, message: str):
        self.message = message


class CancelProductionResult:
    """
    Cancel production response template.
    """
    def __init__(self, message: str):
        self.message = message
