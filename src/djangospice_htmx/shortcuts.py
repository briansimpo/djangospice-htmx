from __future__ import annotations

from django.http import HttpRequest, HttpResponse

from .renderer import ResponseRenderer
from .response import Response

renderer = ResponseRenderer()


def render_response(request: HttpRequest, response: Response | HttpResponse) -> HttpResponse:
    if isinstance(response, Response):
        return renderer.render(response, request)

    return response