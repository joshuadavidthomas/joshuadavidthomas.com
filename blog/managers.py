from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from django.core.paginator import Page
from django.db import models
from django.utils import timezone
from django_twc_toolbox.paginator import DatePaginator

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser

    from users.models import User

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
        self,
        page_number: int | str | None = 1,
        date_field: str = "published_at",
        date_range: datetime.timedelta = datetime.timedelta(days=30),
    ) -> Page["Entry"]:
        print("paginated date_range", date_range)
        paginator = DatePaginator(self, date_field, date_range)

        page_number = page_number or 1
        page_obj = paginator.get_page(int(page_number))

        return page_obj


EntryManager = _EntryManager.from_queryset(EntryQuerySet)
