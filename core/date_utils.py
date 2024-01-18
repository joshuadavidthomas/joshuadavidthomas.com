from __future__ import annotations

import datetime

from django.utils import timezone


def get_range_between_dates(
    min_date: datetime.datetime,
    max_date: datetime.datetime | None = None,
    reverse: bool = False,
) -> list[datetime.date]:
    """Given a min and max date, returns a list of dates between them."""

    if not max_date:
        max_date = timezone.now()

    if max_date <= min_date:
        raise ValueError("max_date must be greater than min_date")

    date_range = [
        min_date.date() + datetime.timedelta(days=n)
        for n in range((max_date - min_date).days + 1)
    ]

    if reverse:
        date_range.reverse()

    return date_range
