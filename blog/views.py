from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from core.date_utils import get_range_between_dates
from core.date_utils import is_same_date_in_timezone
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
    if page_obj.number == 1:
        # if we are on the first page, make sure we include the current day even if there are no entries for today
        max_date = timezone.now()
    date_range = get_range_between_dates(min_date, max_date, reverse=True)

    links = list(
        Link.objects.filter(
            published_at__date__range=[date_range[-1].date(), date_range[0].date()]
        )
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    days = []
    for date in date_range:
        print("date", date)
        day_entries = []
        for entry in page_obj:
            print("entry", entry)
            print("entry.published_at", entry.published_at)
            if entry.published_at and is_same_date_in_timezone(
                entry.published_at, date
            ):
                day_entries.append(entry)
                continue
            if is_same_date_in_timezone(entry.created_at, date):
                day_entries.append(entry)
        day_links = []
        for link in links:
            print("link", link)
            print("link.published_at", link.published_at)
            if link.published_at and is_same_date_in_timezone(link.published_at, date):
                day_links.append(link)
                continue
            if is_same_date_in_timezone(link.created_at, date):
                day_links.append(link)

        items = [(page, "entry") for page in day_entries] + [
            (link, "link") for link in day_links
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
