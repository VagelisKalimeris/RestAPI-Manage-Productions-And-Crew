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
    def __init__(self, message, status=None):
        self.message = message
        self.status = status
