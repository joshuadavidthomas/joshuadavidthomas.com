from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser

    from users.models import User

    from .models import PublishedEntry


class _PublishedEntryManager(models.Manager["PublishedEntry"]):
    def create_duplicate(
        self, entry: PublishedEntry, is_draft: bool = True
    ) -> PublishedEntry:
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


class PublishedEntryQuerySet(models.QuerySet["PublishedEntry"]):
    def for_user(self, user: User | AnonymousUser):
        return self.published()

    def published(self):
        return self.filter(is_draft=False, published_at__lte=timezone.now())

    def drafts(self):
        return self.filter(is_draft=True)

    def chronological(self):
        return self.order_by("published_at")

    def reverse_chronological(self):
        return self.order_by("-published_at")

    def recent_entries(self, count: int = 10):
        return self.published().reverse_chronological()[:count]

    def paginated(
        self, page_number: int | str | None = 1, per_page: int = 10
    ) -> Page["PublishedEntry"]:
        paginator = Paginator(self, per_page)

        page_number = page_number or 1
        page_obj = paginator.get_page(int(page_number))

        return page_obj


PublishedEntryManager = _PublishedEntryManager.from_queryset(PublishedEntryQuerySet)
