from __future__ import annotations

import datetime

from django.db.models import Q
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from core.date_utils import get_range_between_dates
from core.models import get_min_max_of_field

from .models import Entry
from .models import Link
from .models import Tag


def index(request: HttpRequest) -> HttpResponse:
    entries = (
        Entry.objects.for_user(request.user)
        .prefetch_related("tags")
        .reverse_chronological()
    )

    page_obj = entries.paginated(page_number=request.GET.get("page"), per_page=10)

    min_date, max_date = get_min_max_of_field(page_obj.object_list, "created_at")
    date_range = get_range_between_dates(min_date, max_date, reverse=True)

    days = []
    for date in date_range:
        start_of_day = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time.min)
        )
        end_of_day = timezone.make_aware(
            datetime.datetime.combine(date, datetime.time.max)
        )

        day_links = (
            Link.objects.filter(
                Q(published_at__range=(start_of_day, end_of_day))
                | Q(
                    published_at__isnull=True,
                    created_at__range=(start_of_day, end_of_day),
                )
            )
            .prefetch_related("tags")
            .order_by("-created_at")
        )

        day_entries = [page for page in page_obj if page.created_at.date() == date]

        items = [(link, "link") for link in day_links] + [
            (page, "entry") for page in day_entries
        ]
        items.sort(key=lambda item: item[0].created_at, reverse=True)

        days.append({"date": date, "items": items})

    return render(request, "blog/index.html", {"days": days, "page_obj": page_obj})


def entry(request: HttpRequest, year: int, slug: str) -> HttpResponse:
    entry = get_object_or_404(Entry, slug=slug, created_at__year=year)
    return render(request, "blog/entry.html", {"entry": entry})


def tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)
    entries = tag.entry_set.prefetch_related("tags").published().reverse_chronological()  # type: ignore[attr-defined]
    page_obj = entries.paginated(page_number=request.GET.get("page"), per_page=10)
    return render(request, "blog/tag.html", {"tag": tag, "page_obj": page_obj})
