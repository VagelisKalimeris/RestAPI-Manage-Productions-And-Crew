from pydantic import BaseModel


class PaginationResult(BaseModel):
    """
    Response template for pagination results.
    """
    total_records: int
    current_page: int
    total_pages: int
