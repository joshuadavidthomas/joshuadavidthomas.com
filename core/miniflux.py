from __future__ import annotations

import httpx
from django.conf import settings
from django.core.cache import cache


def get_recently_starred_posts(cache_time: int = 60 * 60):
    CACHE_KEY = "miniflux_recently_starred"
    if cache.get(CACHE_KEY):
        posts = cache.get(CACHE_KEY)
    else:
        try:
            posts = httpx.get(
                f"{settings.MINIFLUX['URL'].rstrip('/')}/v1/entries",
                headers={
                    "X-Auth-Token": settings.MINIFLUX["API_KEY"],
                },
                params={
                    "limit": 5,
                    "starred": True,
                },
            ).json()
            cache.set(CACHE_KEY, posts, cache_time)
        except httpx.HTTPError:
            posts = []
    return posts
