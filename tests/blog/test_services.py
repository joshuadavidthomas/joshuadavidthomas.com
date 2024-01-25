from __future__ import annotations

import datetime
import itertools

import pytest
from django.http import HttpRequest
from django.utils import timezone
from model_bakery import baker

from blog.services import PostService

pytestmark = pytest.mark.django_db


class TestPostFeedService:
    def test_get_posts(self):
        NUM_ENTRIES = 10

        baker.make(
            "blog.Entry",
            published_at=itertools.cycle(
                timezone.now() - datetime.timedelta(days=i) for i in range(NUM_ENTRIES)
            ),
            _quantity=NUM_ENTRIES,
        )
        baker.make(
            "blog.Link",
            published_at=itertools.cycle(
                timezone.now() - datetime.timedelta(days=i) for i in range(NUM_ENTRIES)
            ),
            _quantity=NUM_ENTRIES,
        )

        request = HttpRequest()
        request.user = baker.make("users.User")

        dated_items, page_obj = PostService.get_posts(request)

        assert len(dated_items) == NUM_ENTRIES
        assert len(dated_items[0]["items"]) == 2
        assert len(dated_items[1]["items"]) == 2
