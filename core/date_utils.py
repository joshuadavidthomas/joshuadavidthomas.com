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
    source_datetime: datetime.datetime,
    target_datetime: datetime.datetime,
    timezone: str | ZoneInfo | None = None,
) -> bool:
    """Given a datetime object, convert to the given timezone and compare to the target datetime's date.

    By default, we use the timezone defined in settings.TIME_ZONE, but you can pass in a
    timezone string or a ZoneInfo object to override the default.
    """
    if timezone is None:
        timezone = ZoneInfo(settings.TIME_ZONE)
    if isinstance(timezone, str):
        timezone = ZoneInfo(timezone)
    return source_datetime.astimezone(timezone).date() == target_datetime.date()
