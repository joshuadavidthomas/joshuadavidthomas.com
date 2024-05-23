from __future__ import annotations

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Entry
from .models import Tag
from .services import PostService


def index(request: HttpRequest) -> HttpResponse:
    dated_items, page_obj = PostService.get_posts(request)

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
    entries = tag.entry_set.prefetch_related("tags").published().reverse_chronological()
    page_obj = entries.paginated(page_number=request.GET.get("page"), per_page=10)
    return render(request, "blog/tag.html", {"tag": tag, "page_obj": page_obj})
