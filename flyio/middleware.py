from __future__ import annotations

import logging
import sqlite3

from django.db.utils import OperationalError
from django.http import HttpResponse

from .exceptions import WritesAttemptedError
from .machines import get_primary_instance

FLY_REPLAY = "fly-replay"

# Get an instance of a logger
logger = logging.getLogger(__name__)


def replay_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
        except (WritesAttemptedError, sqlite3.OperationalError, OperationalError) as e:
            logger.warning(f"Caught exception in replay middleware: {type(e).__name__}")
            logger.warning(f"Exception details: {str(e)}")

            if isinstance(e, (sqlite3.OperationalError, OperationalError)):
                if "readonly database" not in str(e).lower():
                    logger.error(f"Re-raising non-readonly database error: {str(e)}")
                    raise
                else:
                    logger.info("Handling readonly database error")
            else:
                logger.info("Handling WritesAttemptedError")

            primary = get_primary_instance()
            logger.info(f"Redirecting to primary instance: {primary}")

            response = HttpResponse()
            response[FLY_REPLAY] = f"instance={primary}"

            logger.info(f"Set {FLY_REPLAY} header: {response[FLY_REPLAY]}")
        else:
            logger.debug("Request processed without replay")

        return response

    return middleware


def region_selection_middleware(get_response):
    def middleware(request):
        region = request.GET.get("region")

        if region:
            logger.info(f"Region selection requested: {region}")

            response = HttpResponse()
            replay_header = f"region={region}"
            response[FLY_REPLAY] = replay_header

            logger.info(f"Set {FLY_REPLAY} header: {replay_header}")
            return response

        # If no region is specified, continue with the normal request processing
        response = get_response(request)
        return response

    return middleware
