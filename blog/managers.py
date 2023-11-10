from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.paginator import Page
from django.core.paginator import Paginator
from django.db import models

if TYPE_CHECKING:
    from .models import Entry


class EntryQuerySet(models.QuerySet["Entry"]):
    def published(self):
        return self.filter(is_draft=False)

    def recent_entries(self, count: int = 10):
        return self.published().order_by("-created_at")[:count]

    def paginated(
        self, page_number: int | str | None = 1, per_page: int = 10
    ) -> Page["Entry"]:
        if isinstance(page_number, str):
            page_number = int(page_number)
        elif page_number is None:
            page_number = 1
        paginator = Paginator(self, per_page)
        return paginator.get_page(page_number)
