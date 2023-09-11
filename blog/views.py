from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Entry
from .models import Tag


def index(request: HttpRequest) -> HttpResponse:
    entries = Entry.objects.all().prefetch_related("tags").order_by("-created_at")
    if not request.user.is_staff:
        entries = entries.published()
    page_obj = entries.paginated(page_number=request.GET.get("page"), per_page=10)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def entry(request: HttpRequest, year: int, slug: str) -> HttpResponse:
    entry = get_object_or_404(Entry, slug=slug, created_at__year=year)
    return render(request, "blog/entry.html", {"entry": entry})


def tag(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)
    entries = (
        tag.entry_set.prefetch_related("tags")
        .filter(is_draft=False)
        .order_by("-created_at")
    )
    return render(request, "blog/tag.html", {"tag": tag, "entries": entries})
