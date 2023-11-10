from __future__ import annotations

from django.http import HttpResponse

from .exceptions import WritesAttemptedError
from .machines import get_primary_instance

FLY_REPLAY = "fly-replay"


def replay_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except WritesAttemptedError:
            response = HttpResponse()
            primary = get_primary_instance()
            response[FLY_REPLAY] = f"instance={primary}"
        return response

    return middleware
