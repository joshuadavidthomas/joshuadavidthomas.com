from __future__ import annotations

import sqlite3

from django.db.utils import OperationalError
from django.http import HttpResponse

from .exceptions import WritesAttemptedError
from .machines import get_primary_instance

FLY_REPLAY = "fly-replay"


def replay_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except (WritesAttemptedError, sqlite3.OperationalError, OperationalError) as e:
            if isinstance(e, (sqlite3.OperationalError, OperationalError)):
                if "readonly database" not in str(e).lower():
                    # Re-raise the exception if it's not a readonly database error
                    raise

            response = HttpResponse()
            primary = get_primary_instance()
            response[FLY_REPLAY] = f"instance={primary}"
        return response

    return middleware
