from enum import Enum
from datetime import date

from pydantic import BaseModel, Field, model_validator


class CrewRole(Enum):
    """
    Restricted list of allowed/available roles for new hires.
    """
    Director = 'Director'
    Photographer = 'Photographer'
    Actor = 'Actor'


class CrewMember(BaseModel):
    """
    Purposed for POST request body validation.
    """
    role: CrewRole = Field(json_schema_extra={'example': 'Director'})
    full_name: str = Field(json_schema_extra={'example': 'Quentin Tarantino'})
    hire_date: date
    fire_date: date | None = date.max

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role = self.role.value

    @model_validator(mode='after')
    def dates_are_valid(self):
        if self.hire_date < date.today():
            raise ValueError('Cannot hire member on past date!')
        if self.fire_date <= self.hire_date:
            raise ValueError('Member fire date must be after hire date!')
        return self


class SortCrewBy(str, Enum):
    """
    Purposed for GET request params validation.
    """
    id = 'id'
    name = 'name'
    hire_date = 'hire_date'
    contract_length = 'contract_length'
