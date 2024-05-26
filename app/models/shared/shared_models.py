import json
import typing

from starlette.responses import Response


class PrettyJSONResponse(Response):
    """
    Makes API responses humanly readable.
    """
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(content, ensure_ascii=False, allow_nan=False,
                          indent=2, separators=(", ", ": "), ).encode("utf-8")


class Error:
    """
    Enables easy transfer of errors between layers.
    """
    def __init__(self, message: str, status: int = None):
        self.message = message
        self.status = status


class PaginationResult:
    """
    Response template for pagination results.
    """
    def __init__(self, total_records: int, current_page: int, total_pages: int):
        self.total_records = total_records
        self.current_page = current_page
        self.total_pages = total_pages
