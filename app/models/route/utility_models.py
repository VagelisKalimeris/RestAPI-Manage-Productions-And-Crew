from pydantic import BaseModel


class ApiStatusResult(BaseModel):
    """
    API status response template.
    """
    message: str
