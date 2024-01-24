from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from core.date_utils import get_range_between_dates

from .models import Entry
from .models import Link
from .models import Tag


def index(request: HttpRequest) -> HttpResponse:
    entries = (
        Entry.objects.for_user(request.user)
        .prefetch_related("tags")
        .reverse_chronological()
    )

    page_obj = entries.paginated(page_number=request.GET.get("page"))

    start_date = page_obj.start_date
    end_date = page_obj.end_date
    if start_date == end_date:
        start_date = timezone.now()

    date_range = get_range_between_dates(page_obj.start_date, page_obj.end_date)

    links = list(
        Link.objects.filter(
            published_at__date__range=[date_range[-1].date(), date_range[0].date()]
        )
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    dated_items = []
    for date in date_range:
        items = []
        for link in links:
            if link.published_at and link.published_at.date() == date.date():
                items.append({"type": "link", "entry": link})
        for entry in page_obj.object_list:
            if entry.published_at and entry.published_at.date() == date.date():
                items.append({"type": "entry", "entry": entry})
        dated_items.append({"date": date, "items": items})

    return render(
        request,
        "blog/index.html",
        {
            "dated_items": dated_items,
            "page_obj": page_obj,
        },
    )


def entry(request: HttpRequest, year: int, slug: str) -> HttpResponse:
    entry = get_object_or_404(Entry, slug=slug, created_at__year=year)
    return render(request, "blog/entry.html", {"entry": entry})


def tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)
    entries = tag.entry_set.prefetch_related("tags").published().reverse_chronological()  # type: ignore[attr-defined]
    page_obj = entries.paginated(page_number=request.GET.get("page"), per_page=10)
    return render(request, "blog/tag.html", {"tag": tag, "page_obj": page_obj})
