from __future__ import annotations

import datetime
from zoneinfo import ZoneInfo

from django.conf import settings


def get_range_between_dates(
    min_date: datetime.datetime,
    max_date: datetime.datetime,
    reverse: bool = False,
) -> list[datetime.datetime]:
    """Given a min and max date, returns a list of dates between them.

    We return a list of datetime objects to preserve timezone information.
    """

    if max_date < min_date:
        raise ValueError("max_date must be greater than min_date")

    if max_date.date() == min_date.date():
        return [min_date]

    date_range = [
        min_date + datetime.timedelta(days=n)
        for n in range((max_date - min_date).days + 1)
    ]

    if reverse:
        date_range.reverse()

    return date_range


def is_same_date_in_timezone(
    date1: datetime.datetime,
    date2: datetime.datetime,
    timezone: str | ZoneInfo | None = None,
) -> bool:
    """Given two dates, return True if they are the same date in the given timezone."""
    if timezone is None:
        timezone = ZoneInfo(settings.TIME_ZONE)
    if isinstance(timezone, str):
        timezone = ZoneInfo(timezone)
    return date1.astimezone(timezone).date() == date2.astimezone(timezone).date()
