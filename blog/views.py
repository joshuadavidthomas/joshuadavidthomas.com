from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Entry
from .models import Link
from .models import Tag


def index(request: HttpRequest) -> HttpResponse:
    entries = (
        Entry.objects.for_user(request.user)
        .prefetch_related("tags")
        .reverse_chronological()
    )

    page_obj, date_range = entries.paginated(
        page_number=request.GET.get("page"), per_page=10
    )

    links = (
        Link.objects.filter(published_at__gte=date_range[-1])
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    days = []
    for date in date_range:
        print("date", date)
        day_links = []
        for link in links:
            if (link.published_at and link.published_at.date() == date) or (
                not link.published_at and link.created_at.date() == date
            ):
                day_links.append((link, "link"))
        day_entries = []
        for page in page_obj:
            print("page.created_at", page.created_at.date())
            if page.published_at:
                print("page.published_at", page.published_at.date())
            if (page.published_at and page.published_at.date() == date) or (
                not page.published_at and page.created_at.date() == date
            ):
                day_entries.append((page, "entry"))

        items = day_links + day_entries
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
