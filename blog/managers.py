from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db import models
from django.utils import timezone

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
        if not user.is_staff or not user.is_superuser:
            return self.published()
        return self

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
    ) -> tuple[Page["Entry"], list[datetime.date]]:
        paginator = Paginator(self, per_page)

        page_number = page_number or 1
        page_obj = paginator.get_page(int(page_number))

        datetimes = [entry.created_at for entry in list(page_obj)]
        datetimes.append(timezone.now())

        datetimes = list(set(datetimes))
        datetimes.sort(reverse=True)

        oldest_datetime, newest_datetime = datetimes[-1], datetimes[0]

        date_range = [
            (newest_datetime - datetime.timedelta(days=n)).date()
            for n in range((newest_datetime.date() - oldest_datetime.date()).days + 1)
        ]

        return page_obj, date_range


EntryManager = _EntryManager.from_queryset(EntryQuerySet)
