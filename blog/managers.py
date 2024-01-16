from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from .models import Entry


class _EntryManager(models.Manager["Entry"]):
    def create_duplicate(self, entry: Entry, is_draft: bool = True) -> Entry:
        duplicate = self.create(
            title=f"{entry.title} (copy)",
            slug=f"{entry.slug}-copy",
            summary=entry.summary,
            body=entry.body,
            card_image=entry.card_image,
            is_draft=is_draft,
        )
        duplicate.tags.set(entry.tags.all())
        return duplicate


class EntryQuerySet(models.QuerySet["Entry"]):
    def published(self):
        return self.filter(is_draft=False, published_at__lte=timezone.now())

    def drafts(self):
        return self.filter(is_draft=True)

    def chronological(self):
        return self.order_by("created_at")

    def reverse_chronological(self):
        return self.order_by("-created_at")

    def recent_entries(self, count: int = 10):
        return self.published().reverse_chronological()[:count]

    def paginated(
        self, page_number: int | str | None = 1, per_page: int = 10
    ) -> Page["Entry"]:
        if isinstance(page_number, str):
            page_number = int(page_number)
        elif page_number is None:
            page_number = 1
        paginator = Paginator(self, per_page)
        return paginator.get_page(page_number)


EntryManager = _EntryManager.from_queryset(EntryQuerySet)
